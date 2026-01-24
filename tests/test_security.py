"""Tests for security configuration and validation."""

import sys
from unittest.mock import MagicMock

import pytest

# Mock celery before any imports that might need it
sys.modules["celery"] = MagicMock()

from sono_eval.utils.config import Config  # noqa: E402


class TestSecretValidation:
    """Test security config validation for secrets."""

    def test_secret_validation_in_development_warns(self):
        """Test that default secrets trigger warnings in development."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "development"
        mock_config.secret_key = "your-secret-key-here-change-in-production"
        mock_config.superset_secret_key = "change_this_secret_key_in_production"
        mock_config.allowed_hosts = "*"

        mock_logger = MagicMock()

        original_config = api_main.config
        original_logger = api_main.logger
        try:
            api_main.config = mock_config
            api_main.logger = mock_logger

            # Should not raise in development
            api_main._validate_security_config()

            # Should log warnings
            assert mock_logger.warning.called
        finally:
            api_main.config = original_config
            api_main.logger = original_logger

    def test_secret_validation_production_blocks_default(self):
        """Test that default secrets cause failure in production."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.secret_key = "your-secret-key-here-change-in-production"
        mock_config.superset_secret_key = "valid-superset-key-456-long-enough"
        mock_config.allowed_hosts = "example.com"

        original_config = api_main.config
        try:
            api_main.config = mock_config

            with pytest.raises(ValueError) as exc_info:
                api_main._validate_security_config()

            assert "CRITICAL SECURITY ERROR" in str(exc_info.value)
            assert "SECRET_KEY" in str(exc_info.value)
        finally:
            api_main.config = original_config

    def test_secret_validation_staging_blocks_default(self):
        """Test that default secrets also fail in staging."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "staging"
        mock_config.secret_key = "your-secret-key-here-change-in-production"
        mock_config.superset_secret_key = "valid-superset-key"
        mock_config.allowed_hosts = "*"

        original_config = api_main.config
        try:
            api_main.config = mock_config

            with pytest.raises(ValueError) as exc_info:
                api_main._validate_security_config()

            assert "staging" in str(exc_info.value).lower()
        finally:
            api_main.config = original_config

    def test_secret_validation_production_requires_32_chars(self):
        """Test that short secrets fail in production."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.secret_key = "short-key"  # Less than 32 chars
        mock_config.superset_secret_key = "valid-superset-key-456-long-enough"
        mock_config.allowed_hosts = "example.com"

        original_config = api_main.config
        try:
            api_main.config = mock_config

            with pytest.raises(ValueError) as exc_info:
                api_main._validate_security_config()

            assert "32 characters" in str(exc_info.value)
        finally:
            api_main.config = original_config

    def test_superset_secret_validation_production_fails(self):
        """Test that default Superset secret causes failure in production."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.secret_key = "valid-secret-key-that-is-long-enough-now"
        mock_config.superset_secret_key = "change_this_secret_key_in_production"
        mock_config.allowed_hosts = "example.com"

        original_config = api_main.config
        try:
            api_main.config = mock_config

            with pytest.raises(ValueError) as exc_info:
                api_main._validate_security_config()

            assert "SUPERSET_SECRET_KEY" in str(exc_info.value)
        finally:
            api_main.config = original_config


class TestCorsValidation:
    """Test CORS configuration validation."""

    def test_cors_production_requires_allowed_hosts(self):
        """Test that wildcard CORS fails in production."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.secret_key = "valid-secret-key-that-is-long-enough-now"
        mock_config.superset_secret_key = "valid-superset-key-456-long-enough"
        mock_config.allowed_hosts = "*"

        original_config = api_main.config
        try:
            api_main.config = mock_config

            with pytest.raises(ValueError) as exc_info:
                api_main._validate_security_config()

            assert "ALLOWED_HOSTS" in str(exc_info.value)
        finally:
            api_main.config = original_config

    def test_cors_staging_warns_for_wildcard(self):
        """Test that wildcard CORS warns in staging."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "staging"
        mock_config.secret_key = "valid-secret-key-that-is-long-enough-now"
        mock_config.superset_secret_key = "valid-superset-key-456-long-enough"
        mock_config.allowed_hosts = "*"

        mock_logger = MagicMock()

        original_config = api_main.config
        original_logger = api_main.logger
        try:
            api_main.config = mock_config
            api_main.logger = mock_logger

            # Should not raise in staging, just warn
            api_main._validate_security_config()

            # Should log warning about ALLOWED_HOSTS
            warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
            assert any("ALLOWED_HOSTS" in call for call in warning_calls)
        finally:
            api_main.config = original_config
            api_main.logger = original_logger

    def test_valid_production_config_passes(self):
        """Test that valid production config passes validation."""
        import sono_eval.api.main as api_main

        mock_config = MagicMock()
        mock_config.app_env = "production"
        mock_config.secret_key = "valid-secret-key-that-is-long-enough-now"
        mock_config.superset_secret_key = "valid-superset-key-456-long-enough"
        mock_config.allowed_hosts = "example.com,api.example.com"

        mock_logger = MagicMock()

        original_config = api_main.config
        original_logger = api_main.logger
        try:
            api_main.config = mock_config
            api_main.logger = mock_logger

            # Should not raise with valid config
            api_main._validate_security_config()
        finally:
            api_main.config = original_config
            api_main.logger = original_logger


class TestConfigFieldConstraints:
    """Test configuration field validations."""

    def test_config_defaults(self):
        """Test configuration default values."""
        config = Config()

        assert config.api_port == 8000
        assert config.api_workers == 4
        assert config.max_upload_size == 10485760  # 10MB

    def test_config_field_types(self):
        """Test that fields are properly typed."""
        config = Config()

        assert isinstance(config.api_port, int)
        assert isinstance(config.debug, bool)
        assert isinstance(config.allowed_hosts, str)

    def test_allowed_hosts_parsing(self):
        """Test that allowed hosts have sensible defaults."""
        config = Config()

        # Default should include localhost
        assert "localhost" in config.allowed_hosts
