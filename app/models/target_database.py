import re
from enum import StrEnum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class TargetEnvironment(StrEnum):
    LOCAL = "Local"
    DEVELOPMENT = "Development"
    STAGING = "Staging"
    PRODUCTION = "Production"
    OTHER = "Other"


_REFERENCE_HOSTS = {
    "laptop-h752smp0",
    "127.0.0.1",
    "localhost",
    "::1",
    "[::1]",
}
PROTECTED_REFERENCE_DATABASE = "db_solog_oli_initial"
_REFERENCE_PORT = 3306


def is_protected_reference_identity(host: str, port: int, database: str) -> bool:
    normalized_host = host.strip().casefold().rstrip(".")
    normalized_database = database.strip().casefold()
    return (
        normalized_host in _REFERENCE_HOSTS
        and port == _REFERENCE_PORT
        and normalized_database == PROTECTED_REFERENCE_DATABASE
    )


class TargetDatabaseProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile_id: UUID = Field(default_factory=uuid4)
    revision: int = Field(default=0, ge=0)
    name: str = Field(min_length=1, max_length=80)
    environment: TargetEnvironment
    host: str = Field(min_length=1, max_length=253)
    port: int = Field(ge=1, le=65535, strict=True)
    database: str = Field(min_length=1, max_length=64)
    username: str = Field(min_length=1, max_length=128)
    purpose: str = Field(default="TARGET", pattern="^TARGET$")

    @field_validator("name", "host", "database", "username", mode="before")
    @classmethod
    def strip_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Nama profil wajib diisi.")
        if any(ord(character) < 32 for character in value):
            raise ValueError("Nama profil mengandung karakter kontrol.")
        return value

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        if not value or len(value) > 253:
            raise ValueError("Host wajib diisi dan maksimal 253 karakter.")
        if any(character.isspace() or ord(character) < 32 for character in value):
            raise ValueError("Host tidak valid.")
        if any(character in value for character in "/\\@"):
            raise ValueError("Host tidak valid.")
        return value

    @field_validator("database")
    @classmethod
    def validate_database_name(cls, value: str) -> str:
        if not value or len(value) > 64:
            raise ValueError("Nama database wajib diisi dan maksimal 64 karakter.")
        if not re.fullmatch(r"[A-Za-z0-9_$-]+", value):
            raise ValueError("Nama database berisi karakter yang tidak didukung.")
        return value

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value or len(value) > 128:
            raise ValueError("Username wajib diisi dan maksimal 128 karakter.")
        if (
            "@" in value
            or any(character.isspace() or ord(character) < 32 for character in value)
        ):
            raise ValueError("Username tidak valid.")
        return value

    @model_validator(mode="after")
    def reject_reference_database(self) -> "TargetDatabaseProfile":
        if is_protected_reference_identity(self.host, self.port, self.database):
            raise ValueError(
                "Identitas database referensi tidak dapat digunakan sebagai TARGET."
            )
        return self


class TargetDatabaseConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    profiles: list[TargetDatabaseProfile] = Field(default_factory=list)
    selected_profile_id: UUID | None = None

    @model_validator(mode="after")
    def validate_profiles_and_selection(self) -> "TargetDatabaseConfiguration":
        profile_ids = [profile.profile_id for profile in self.profiles]
        if len(profile_ids) != len(set(profile_ids)):
            raise ValueError("ID profil target harus unik.")
        names = [profile.name.casefold() for profile in self.profiles]
        if len(names) != len(set(names)):
            raise ValueError("Nama profil target harus unik.")
        if (
            self.selected_profile_id is not None
            and self.selected_profile_id not in set(profile_ids)
        ):
            raise ValueError("Profil target terpilih tidak ditemukan.")
        return self
