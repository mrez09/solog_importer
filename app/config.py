from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


class Settings(BaseSettings):
    """Runtime settings for the local importer UI; deliberately has no DB settings."""

    app_name: str = "Solog OLI Migration Importer"
    environment: str = "local"
    debug: bool = False
    max_upload_size_bytes: int = Field(default=100 * 1024 * 1024, gt=0)

    model_config = SettingsConfigDict(
        env_prefix="SOLOG_IMPORTER_",
        env_file=None,
        extra="ignore",
    )


settings = Settings()
