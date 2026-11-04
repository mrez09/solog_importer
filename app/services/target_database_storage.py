import json
import os
from pathlib import Path
import tempfile
from uuid import UUID

from pydantic import ValidationError

from app.config import DATA_DIR
from app.models.target_database import (
    TargetDatabaseConfiguration,
    TargetDatabaseProfile,
)


class TargetDatabaseStorageError(Exception):
    """Raised when target profile metadata cannot be safely read or saved."""


class TargetDatabaseProfileNotFoundError(Exception):
    """Raised when a requested target profile does not exist."""


class TargetDatabaseProfileConflictError(Exception):
    """Raised when a target profile name is already in use."""


class TargetDatabaseStorage:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR
        self.configuration_path = self.data_dir / "target-databases.json"

    def load(self) -> TargetDatabaseConfiguration:
        self._validate_directory(create=False)
        if not self.configuration_path.exists():
            return TargetDatabaseConfiguration()
        if self.configuration_path.is_symlink() or not self.configuration_path.is_file():
            raise TargetDatabaseStorageError(
                "Berkas konfigurasi target bukan file lokal reguler."
            )
        try:
            return TargetDatabaseConfiguration.model_validate_json(
                self.configuration_path.read_text(encoding="utf-8")
            )
        except (OSError, UnicodeDecodeError, ValidationError, ValueError) as exc:
            raise TargetDatabaseStorageError(
                "Konfigurasi target lokal rusak atau tidak valid."
            ) from exc

    def create(self, profile: TargetDatabaseProfile) -> None:
        configuration = self.load()
        self._ensure_unique_name(configuration, profile.name)
        configuration.profiles.append(profile)
        self.save(configuration)

    def update(self, profile: TargetDatabaseProfile) -> None:
        configuration = self.load()
        existing_index = self._find_index(configuration, profile.profile_id)
        self._ensure_unique_name(
            configuration,
            profile.name,
            excluding=profile.profile_id,
        )
        configuration.profiles[existing_index] = profile.model_copy(
            update={
                "revision": configuration.profiles[existing_index].revision + 1,
            }
        )
        self.save(configuration)

    def select(self, profile_id: UUID) -> None:
        configuration = self.load()
        self._find_index(configuration, profile_id)
        configuration.selected_profile_id = profile_id
        self.save(configuration)

    def delete(self, profile_id: UUID) -> None:
        configuration = self.load()
        existing_index = self._find_index(configuration, profile_id)
        del configuration.profiles[existing_index]
        if configuration.selected_profile_id == profile_id:
            configuration.selected_profile_id = None
        self.save(configuration)

    def save(self, configuration: TargetDatabaseConfiguration) -> None:
        self._validate_directory(create=True)
        if self.configuration_path.is_symlink():
            raise TargetDatabaseStorageError(
                "Berkas konfigurasi target tidak boleh berupa symlink."
            )
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".target-databases-",
            suffix=".tmp",
            dir=self.data_dir,
        )
        temporary_path = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as target:
                json.dump(
                    configuration.model_dump(mode="json"),
                    target,
                    ensure_ascii=False,
                    indent=2,
                )
            os.replace(temporary_path, self.configuration_path)
        except OSError as exc:
            raise TargetDatabaseStorageError(
                "Konfigurasi target lokal tidak dapat disimpan."
            ) from exc
        finally:
            temporary_path.unlink(missing_ok=True)

    @staticmethod
    def _find_index(
        configuration: TargetDatabaseConfiguration,
        profile_id: UUID,
    ) -> int:
        for index, profile in enumerate(configuration.profiles):
            if profile.profile_id == profile_id:
                return index
        raise TargetDatabaseProfileNotFoundError(
            "Profil target tidak ditemukan."
        )

    @staticmethod
    def _ensure_unique_name(
        configuration: TargetDatabaseConfiguration,
        name: str,
        *,
        excluding: UUID | None = None,
    ) -> None:
        normalized_name = name.casefold()
        if any(
            profile.profile_id != excluding
            and profile.name.casefold() == normalized_name
            for profile in configuration.profiles
        ):
            raise TargetDatabaseProfileConflictError(
                "Nama profil target sudah digunakan."
            )

    def _validate_directory(self, *, create: bool) -> None:
        if create:
            try:
                self.data_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise TargetDatabaseStorageError(
                    "Direktori data lokal tidak dapat disiapkan."
                ) from exc
        if not self.data_dir.exists():
            return
        if self.data_dir.is_symlink() or not self.data_dir.is_dir():
            raise TargetDatabaseStorageError(
                "Direktori data harus berupa direktori lokal reguler."
            )
