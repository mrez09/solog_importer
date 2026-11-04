import json
import os
from pathlib import Path
import tempfile

from pydantic import ValidationError

from app.config import DATA_DIR
from app.models.mapping import MappingProfile


class MappingStorageError(Exception):
    """Raised when a local mapping profile is unavailable or invalid."""


class MappingStorage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.mapping_dir = (data_dir or DATA_DIR) / "mappings"

    def load_profile(self, source_file_id: str, source_sha256: str) -> MappingProfile:
        path = self._profile_path(source_file_id)
        if not path.exists():
            return MappingProfile(
                source_file_id=source_file_id,
                source_sha256=source_sha256,
            )
        if path.is_symlink() or not path.is_file():
            raise MappingStorageError("Berkas profil mapping bukan file reguler.")
        try:
            profile = MappingProfile.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValidationError, ValueError) as exc:
            raise MappingStorageError("Profil mapping lokal rusak atau tidak valid.") from exc
        if (
            profile.source_file_id != source_file_id
            or profile.source_sha256 != source_sha256
        ):
            raise MappingStorageError(
                "Identitas sumber atau fingerprint profil mapping tidak cocok."
            )
        return profile

    def save_profile(self, profile: MappingProfile) -> None:
        self._validate_directory(create=True)
        path = self._profile_path(profile.source_file_id)
        if path.is_symlink():
            raise MappingStorageError("Profil mapping tidak boleh berupa symlink.")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".mapping-",
            suffix=".tmp",
            dir=self.mapping_dir,
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as target:
                json.dump(
                    profile.model_dump(mode="json"),
                    target,
                    ensure_ascii=False,
                    indent=2,
                )
            os.replace(temporary_path, path)
        except OSError as exc:
            raise MappingStorageError("Profil mapping lokal tidak dapat disimpan.") from exc
        finally:
            temporary_path.unlink(missing_ok=True)

    def _profile_path(self, source_file_id: str) -> Path:
        if (
            len(source_file_id) != 32
            or any(character not in "0123456789abcdef" for character in source_file_id)
        ):
            raise MappingStorageError("Identitas sumber mapping tidak valid.")
        self._validate_directory(create=False)
        return self.mapping_dir / f"{source_file_id}.json"

    def _validate_directory(self, *, create: bool) -> None:
        if create:
            try:
                self.mapping_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise MappingStorageError(
                    "Direktori profil mapping tidak dapat disiapkan."
                ) from exc
        if not self.mapping_dir.exists():
            return
        if self.mapping_dir.is_symlink() or not self.mapping_dir.is_dir():
            raise MappingStorageError(
                "Direktori profil mapping harus berupa direktori lokal reguler."
            )
