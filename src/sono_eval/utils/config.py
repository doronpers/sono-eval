"""Configuration management for Sono-Eval."""

from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # Application
    app_name: str = Field(default="sono-eval", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # API Server
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")  # nosec B104
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
    # Dark Horse mode: Set to "disabled" for public release to avoid licensing concerns
    # See DARK_HORSE_MITIGATION.md for details
    dark_horse_mode: str = Field(default="enabled", alias="DARK_HORSE_MODE")
    pattern_checks_enabled: bool = Field(default=True, alias="PATTERN_CHECKS_ENABLED")
    pattern_penalty_low: float = Field(default=1.0, alias="PATTERN_PENALTY_LOW")
    pattern_penalty_medium: float = Field(default=3.0, alias="PATTERN_PENALTY_MEDIUM")
    pattern_penalty_high: float = Field(default=6.0, alias="PATTERN_PENALTY_HIGH")
    pattern_penalty_max: float = Field(default=15.0, alias="PATTERN_PENALTY_MAX")

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

    def validate_production_config(self) -> None:
        """
        Validate configuration for production environment.

        Raises:
            ValueError: If production configuration is invalid
        """
        if self.app_env == "production":
            # Validate DATABASE_URL is not using default SQLite path
            if (
                self.database_url.startswith("sqlite:///./")
                or self.database_url == "sqlite:///./sono_eval.db"
            ):
                raise ValueError(
                    "CRITICAL: DATABASE_URL must not use default SQLite path in production. "
                    "Use PostgreSQL or a properly configured database. "
                    "Set DATABASE_URL to a production database connection string."
                )

    @classmethod
    def get_preset(cls, preset_name: str) -> Dict[str, Any]:
        """
        Get configuration preset values with optimized settings for different use cases.

        Presets:
        - quick_test: Fast setup for quick testing (minimal features, fast startup)
        - development: Full-featured development environment (all features enabled)
        - testing: Optimized for running tests (fast, minimal resources)
        - staging: Pre-production environment (production-like but with debugging)
        - production: Production-ready configuration (optimized, secure)
        - high_performance: Maximum performance (more workers, aggressive caching)
        - low_resource: Minimal resource usage (single worker, no ML models)
        - ml_development: ML model development and training (ML features enabled)

        Args:
            preset_name: Name of the preset

        Returns:
            Dictionary of configuration values to set as environment variables

        Example:
            ```python
            preset = Config.get_preset("development")
            # Set environment variables from preset
            for key, value in preset.items():
                os.environ[key] = str(value)
            ```
        """
        presets = {
            "quick_test": {
                "APP_ENV": "development",
                "DEBUG": True,
                "LOG_LEVEL": "ERROR",  # Minimal logging
                "API_WORKERS": 1,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": False,  # Faster
                "ASSESSMENT_MULTI_PATH_TRACKING": False,  # Single path only
                "DARK_HORSE_MODE": "disabled",
                "TAGSTUDIO_AUTO_TAG": False,
                "MEMU_CACHE_SIZE": 100,  # Small cache
                "MAX_CONCURRENT_ASSESSMENTS": 1,
                "BATCH_SIZE": 8,
            },
            "development": {
                "APP_ENV": "development",
                "DEBUG": True,
                "LOG_LEVEL": "INFO",
                "API_WORKERS": 2,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": True,
                "MEMU_CACHE_SIZE": 500,
                "MAX_CONCURRENT_ASSESSMENTS": 2,
                "BATCH_SIZE": 16,
                "T5_MODEL_NAME": "t5-base",  # Standard model
            },
            "testing": {
                "APP_ENV": "testing",
                "DEBUG": False,
                "LOG_LEVEL": "WARNING",  # Less verbose in tests
                "API_WORKERS": 1,
                "API_PORT": 8001,  # Different port to avoid conflicts
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": False,  # Skip auto-tagging in tests
                "MEMU_CACHE_SIZE": 50,
                "MAX_CONCURRENT_ASSESSMENTS": 1,
                "BATCH_SIZE": 4,
                "DATABASE_URL": "sqlite:///:memory:",  # In-memory DB for tests
            },
            "staging": {
                "APP_ENV": "staging",
                "DEBUG": False,
                "LOG_LEVEL": "INFO",
                "API_WORKERS": 3,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": True,
                "MEMU_CACHE_SIZE": 2000,
                "MAX_CONCURRENT_ASSESSMENTS": 4,
                "BATCH_SIZE": 32,
                # Security: Must be set explicitly
                "ALLOWED_HOSTS": "",  # Must configure
                "SECRET_KEY": "",  # Must set strong key
            },
            "production": {
                "APP_ENV": "production",
                "DEBUG": False,
                "LOG_LEVEL": "INFO",
                "API_WORKERS": 4,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": True,
                "MEMU_CACHE_SIZE": 5000,
                "MAX_CONCURRENT_ASSESSMENTS": 8,
                "BATCH_SIZE": 64,
                # Security: Must be set explicitly
                "ALLOWED_HOSTS": "",  # Must configure specific domains
                "SECRET_KEY": "",  # Must set strong key
                "SUPERSET_SECRET_KEY": "",  # Must set strong key
                "DATABASE_URL": "",  # Must use PostgreSQL
            },
            "high_performance": {
                "APP_ENV": "production",
                "DEBUG": False,
                "LOG_LEVEL": "WARNING",  # Less logging overhead
                "API_WORKERS": 8,  # More workers
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": True,
                "MEMU_CACHE_SIZE": 10000,  # Large cache
                "MAX_CONCURRENT_ASSESSMENTS": 16,  # High concurrency
                "BATCH_SIZE": 128,  # Large batches
            },
            "low_resource": {
                "APP_ENV": "development",
                "DEBUG": True,
                "LOG_LEVEL": "ERROR",
                "API_WORKERS": 1,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": False,  # Single path
                "DARK_HORSE_MODE": "disabled",
                "TAGSTUDIO_AUTO_TAG": False,
                "MEMU_CACHE_SIZE": 50,  # Minimal cache
                "MAX_CONCURRENT_ASSESSMENTS": 1,
                "BATCH_SIZE": 4,
                "T5_MODEL_NAME": "t5-small",  # Smaller model
            },
            "ml_development": {
                "APP_ENV": "development",
                "DEBUG": True,
                "LOG_LEVEL": "DEBUG",  # Verbose for ML debugging
                "API_WORKERS": 2,
                "API_PORT": 8000,
                "ASSESSMENT_ENABLE_EXPLANATIONS": True,
                "ASSESSMENT_MULTI_PATH_TRACKING": True,
                "DARK_HORSE_MODE": "enabled",
                "TAGSTUDIO_AUTO_TAG": True,
                "MEMU_CACHE_SIZE": 1000,
                "MAX_CONCURRENT_ASSESSMENTS": 2,
                "BATCH_SIZE": 16,
                "T5_MODEL_NAME": "t5-base",
                "T5_LORA_RANK": 16,  # Higher rank for training
                "T5_LORA_ALPHA": 32,
            },
        }

        if preset_name not in presets:
            available = ", ".join(presets.keys())
            raise ValueError(
                f"Unknown preset: '{preset_name}'. "
                f"Available presets: {available}\n\n"
                f"Preset descriptions:\n"
                f"  - quick_test: Fast setup for quick testing\n"
                f"  - development: Full-featured development environment\n"
                f"  - testing: Optimized for running tests\n"
                f"  - staging: Pre-production environment\n"
                f"  - production: Production-ready configuration\n"
                f"  - high_performance: Maximum performance settings\n"
                f"  - low_resource: Minimal resource usage\n"
                f"  - ml_development: ML model development and training"
            )

        return presets[preset_name]

    @classmethod
    def list_presets(cls) -> Dict[str, str]:
        """
        List all available configuration presets with descriptions.

        Returns:
            Dictionary mapping preset names to descriptions
        """
        return {
            "quick_test": "Fast setup for quick testing (minimal features, fast startup)",
            "development": "Full-featured development environment (all features enabled)",
            "testing": "Optimized for running tests (fast, minimal resources)",
            "staging": "Pre-production environment (production-like but with debugging)",
            "production": "Production-ready configuration (optimized, secure)",
            "high_performance": "Maximum performance (more workers, aggressive caching)",
            "low_resource": "Minimal resource usage (single worker, no ML models)",
            "ml_development": "ML model development and training (ML features enabled)",
        }


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config
