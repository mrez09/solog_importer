import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi import UploadFile
from pydantic import ValidationError

from app.config import DATA_DIR, PROJECT_ROOT, settings
from app.models.workbook import WorkbookRecord, WorksheetPage
from app.services.xlsx_reader import (
    WorkbookDetail,
    WorkbookReadError,
    inspect_workbook,
    read_worksheet_page,
)

CHUNK_SIZE = 64 * 1024


class UploadRejectedError(Exception):
    """Raised when an uploaded source file does not meet the XLSX upload policy."""


class WorkbookStorageError(Exception):
    """Raised when local workbook metadata or stored source files are unavailable."""


class WorkbookStorage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.upload_dir = (data_dir or DATA_DIR) / "uploads"

    async def save_upload(self, upload: UploadFile) -> WorkbookRecord:
        filename = upload.filename
        if not filename or Path(filename).suffix.casefold() != ".xlsx":
            raise UploadRejectedError("Hanya berkas berekstensi .xlsx yang dapat diunggah.")

        try:
            self.upload_dir.mkdir(parents=True, exist_ok=True)
            _validate_storage_directory(self.upload_dir)
        except OSError as exc:
            raise WorkbookStorageError("Direktori penyimpanan workbook tidak dapat disiapkan.") from exc
        temporary_path: Path | None = None
        source_path: Path | None = None
        metadata_path: Path | None = None
        source_created = False
        metadata_created = False

        try:
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=".upload-",
                suffix=".xlsx",
                dir=self.upload_dir,
            )
            temporary_path = Path(temporary_name)
            digest = hashlib.sha256()
            size_bytes = 0
            with os.fdopen(descriptor, "wb") as destination:
                while chunk := await upload.read(CHUNK_SIZE):
                    size_bytes += len(chunk)
                    if size_bytes > settings.max_upload_size_bytes:
                        raise UploadRejectedError(
                            "Ukuran berkas melebihi batas "
                            f"{settings.max_upload_size_bytes:,} bytes."
                        )
                    digest.update(chunk)
                    destination.write(chunk)

            if size_bytes == 0:
                raise UploadRejectedError("Berkas kosong tidak dapat dibaca sebagai workbook.")

            source_file_id = uuid4().hex
            storage_filename = f"{source_file_id}.xlsx"
            source_path = self.upload_dir / storage_filename
            metadata_path = self.upload_dir / f"{source_file_id}.json"

            initial_record = WorkbookRecord(
                source_file_id=source_file_id,
                source_filename=filename,
                storage_filename=storage_filename,
                source_sha256=digest.hexdigest(),
                size_bytes=size_bytes,
                uploaded_at=datetime.now(UTC),
                read_status="readable",
            )
            inspect_workbook(temporary_path, initial_record)
            _copy_exclusive(temporary_path, source_path)
            source_created = True
            _write_json_exclusive(metadata_path, initial_record.model_dump(mode="json"))
            metadata_created = True
            return initial_record
        except UploadRejectedError:
            raise
        except WorkbookReadError as exc:
            raise UploadRejectedError(str(exc)) from exc
        except OSError as exc:
            raise WorkbookStorageError("Penyimpanan lokal workbook gagal.") from exc
        finally:
            try:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
                if source_created and not metadata_created and source_path is not None:
                    source_path.unlink(missing_ok=True)
            except OSError as exc:
                raise WorkbookStorageError("Pembersihan file sementara upload gagal.") from exc

    def list_workbooks(self) -> list[WorkbookRecord]:
        try:
            if not self.upload_dir.exists():
                return []
            _validate_storage_directory(self.upload_dir)

            records: list[WorkbookRecord] = []
            for metadata_path in self.upload_dir.glob("*.json"):
                if metadata_path.is_symlink():
                    raise WorkbookStorageError("Metadata workbook tidak boleh berupa symlink.")
                try:
                    record = WorkbookRecord.model_validate_json(metadata_path.read_text(encoding="utf-8"))
                    if metadata_path.stem != record.source_file_id:
                        raise WorkbookStorageError("Identitas metadata workbook tidak cocok dengan namanya.")
                    _validate_id(record.source_file_id)
                    records.append(record)
                except (OSError, UnicodeDecodeError, ValidationError, ValueError) as exc:
                    raise WorkbookStorageError(
                        f"Metadata workbook {metadata_path.name} rusak atau tidak valid."
                    ) from exc
            return sorted(records, key=lambda record: record.uploaded_at, reverse=True)
        except WorkbookStorageError:
            raise
        except OSError as exc:
            raise WorkbookStorageError("Penyimpanan metadata workbook tidak dapat dibaca.") from exc

    def get_workbook(self, source_file_id: str) -> WorkbookRecord:
        source_file_id = _validate_id(source_file_id)
        _validate_storage_directory(self.upload_dir)
        metadata_path = self.upload_dir / f"{source_file_id}.json"
        if not metadata_path.is_file() or metadata_path.is_symlink():
            raise FileNotFoundError(source_file_id)
        try:
            record = WorkbookRecord.model_validate_json(metadata_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValidationError) as exc:
            raise WorkbookStorageError("Metadata workbook rusak atau tidak valid.") from exc
        if record.source_file_id != source_file_id:
            raise WorkbookStorageError("Identitas metadata workbook tidak cocok.")
        return record

    def inspect(self, source_file_id: str) -> WorkbookDetail:
        return self.inspect_record(self.get_workbook(source_file_id))

    def inspect_record(self, record: WorkbookRecord) -> WorkbookDetail:
        source_path = self._verified_source_path(record)
        return inspect_workbook(source_path, record)

    def read_sheet_page(
        self,
        record: WorkbookRecord,
        sheet_index: int,
        start_row: int,
        start_column: int,
    ) -> WorksheetPage:
        source_path = self._verified_source_path(record)
        return read_worksheet_page(
            source_path,
            record,
            sheet_index,
            start_row,
            start_column,
        )

    def update_read_error(self, source_file_id: str, message: str) -> WorkbookRecord:
        record = self.get_workbook(source_file_id)
        updated_record = record.model_copy(
            update={"read_status": "error", "read_error": message}
        )
        metadata_path = self.upload_dir / f"{source_file_id}.json"
        try:
            _replace_json(metadata_path, updated_record.model_dump(mode="json"))
        except OSError as exc:
            raise WorkbookStorageError("Status baca workbook tidak dapat disimpan.") from exc
        return updated_record

    def _verified_source_path(self, record: WorkbookRecord) -> Path:
        _validate_storage_directory(self.upload_dir)
        source_path = self.upload_dir / record.storage_filename
        if source_path.is_symlink() or not source_path.is_file():
            raise FileNotFoundError(record.source_file_id)
        try:
            actual_hash = _sha256_file(source_path)
        except OSError as exc:
            raise WorkbookStorageError("Salinan workbook tidak dapat dibaca dari penyimpanan.") from exc
        if actual_hash != record.source_sha256:
            raise WorkbookStorageError("Hash workbook berubah setelah diunggah; sumber tidak dibaca.")
        return source_path


def _validate_id(source_file_id: str) -> str:
    try:
        return UUID(source_file_id).hex
    except ValueError as exc:
        raise FileNotFoundError(source_file_id) from exc


def _validate_storage_directory(path: Path) -> None:
    try:
        if path.is_symlink() or path.parent.is_symlink():
            raise WorkbookStorageError("Direktori penyimpanan workbook tidak boleh berupa symlink.")
        project_root = PROJECT_ROOT.resolve()
        path.resolve().relative_to(project_root)
    except ValueError as exc:
        raise WorkbookStorageError("Penyimpanan workbook harus berada di dalam workspace importer.") from exc
    except (OSError, RuntimeError) as exc:
        raise WorkbookStorageError("Direktori penyimpanan workbook tidak valid.") from exc


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_exclusive(source: Path, destination: Path) -> None:
    descriptor = os.open(
        destination,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        with os.fdopen(descriptor, "wb") as target, source.open("rb") as origin:
            shutil.copyfileobj(origin, target, length=CHUNK_SIZE)
    except OSError:
        destination.unlink(missing_ok=True)
        raise


def _write_json_exclusive(path: Path, data: dict[str, object]) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as target:
            json.dump(data, target, ensure_ascii=False, indent=2)
    except OSError:
        path.unlink(missing_ok=True)
        raise


def _replace_json(path: Path, data: dict[str, object]) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".metadata-",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as target:
            json.dump(data, target, ensure_ascii=False, indent=2)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)
