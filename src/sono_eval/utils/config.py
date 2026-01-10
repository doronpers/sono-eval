"""Configuration management for Sono-Eval."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Application
    app_name: str = Field(default="sono-eval", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # API Server
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_workers: int = Field(default=4, alias="API_WORKERS")

    # Database
    database_url: str = Field(default="sqlite:///./sono_eval.db", alias="DATABASE_URL")

    # Redis
    redis_host: str = Field(default="localhost", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, alias="REDIS_PASSWORD")

    # MemU Configuration
    memu_storage_path: str = Field(default="./data/memory", alias="MEMU_STORAGE_PATH")
    memu_max_depth: int = Field(default=5, alias="MEMU_MAX_DEPTH")
    memu_cache_size: int = Field(default=1000, alias="MEMU_CACHE_SIZE")

    # T5 Model Configuration
    t5_model_name: str = Field(default="t5-base", alias="T5_MODEL_NAME")
    t5_cache_dir: str = Field(default="./models/cache", alias="T5_CACHE_DIR")
    t5_lora_rank: int = Field(default=8, alias="T5_LORA_RANK")
    t5_lora_alpha: int = Field(default=16, alias="T5_LORA_ALPHA")
    t5_lora_dropout: float = Field(default=0.1, alias="T5_LORA_DROPOUT")

    # TagStudio Configuration
    tagstudio_root: str = Field(default="./data/tagstudio", alias="TAGSTUDIO_ROOT")
    tagstudio_auto_tag: bool = Field(default=True, alias="TAGSTUDIO_AUTO_TAG")

    # Assessment Configuration
    assessment_engine_version: str = Field(default="1.0", alias="ASSESSMENT_ENGINE_VERSION")
    assessment_enable_explanations: bool = Field(
        default=True, alias="ASSESSMENT_ENABLE_EXPLANATIONS"
    )
    assessment_multi_path_tracking: bool = Field(
        default=True, alias="ASSESSMENT_MULTI_PATH_TRACKING"
    )
    dark_horse_mode: str = Field(default="enabled", alias="DARK_HORSE_MODE")

    # Superset Configuration
    superset_host: str = Field(default="localhost", alias="SUPERSET_HOST")
    superset_port: int = Field(default=8088, alias="SUPERSET_PORT")
    superset_secret_key: str = Field(
        default="change_this_secret_key_in_production", alias="SUPERSET_SECRET_KEY"
    )

    # Security
    secret_key: str = Field(default="your-secret-key-here-change-in-production", alias="SECRET_KEY")
    allowed_hosts: str = Field(default="localhost,127.0.0.1", alias="ALLOWED_HOSTS")

    # File Upload
    max_upload_size: int = Field(default=10485760, alias="MAX_UPLOAD_SIZE")
    allowed_extensions: str = Field(
        default="py,js,ts,java,cpp,c,go,rs,rb", alias="ALLOWED_EXTENSIONS"
    )

    # Batch Processing
    batch_size: int = Field(default=32, alias="BATCH_SIZE")
    max_concurrent_assessments: int = Field(default=4, alias="MAX_CONCURRENT_ASSESSMENTS")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_storage_path(self) -> Path:
        """Get the storage path for memory data."""
        path = Path(self.memu_storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_cache_dir(self) -> Path:
        """Get the cache directory for models."""
        path = Path(self.t5_cache_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_tagstudio_root(self) -> Path:
        """Get the TagStudio root directory."""
        path = Path(self.tagstudio_root)
        path.mkdir(parents=True, exist_ok=True)
        return path


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
