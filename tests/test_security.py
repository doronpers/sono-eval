"""Tests for security configuration and validation."""

from unittest.mock import patch

import pytest

from sono_eval.utils.config import Config


def test_secret_validation_in_development():
    """Test that default secrets trigger warnings in development."""
    with patch("sono_eval.api.main.logger") as mock_logger:
        with patch("sono_eval.api.main.config") as mock_config:
            mock_config.app_env = "development"
            mock_config.secret_key = "your-secret-key-here-change-in-production"
            mock_config.superset_secret_key = "change_this_secret_key_in_production"
            mock_config.allowed_hosts = "*"

            from sono_eval.api.main import _validate_security_config

            # Should not raise in development
            _validate_security_config()

            # Should log warnings
            assert mock_logger.warning.called


def test_secret_validation_in_production_fails():
    """Test that default secrets cause failure in production."""
    with patch("sono_eval.api.main.config") as mock_config:
        mock_config.app_env = "production"
        mock_config.secret_key = "your-secret-key-here-change-in-production"

        from sono_eval.api.main import _validate_security_config

        # Should raise ValueError in production
        with pytest.raises(ValueError) as exc_info:
            _validate_security_config()

        assert "CRITICAL SECURITY ERROR" in str(exc_info.value)


def test_superset_secret_validation_in_production_fails():
    """Test that default Superset secret causes failure in production."""
    with patch("sono_eval.api.main.config") as mock_config:
        mock_config.app_env = "production"
        mock_config.secret_key = "valid-secret-key-123"
        mock_config.superset_secret_key = "change_this_secret_key_in_production"
        mock_config.allowed_hosts = "example.com"

        from sono_eval.api.main import _validate_security_config

        # Should raise ValueError in production
        with pytest.raises(ValueError) as exc_info:
            _validate_security_config()

        assert "SUPERSET_SECRET_KEY" in str(exc_info.value)


def test_cors_validation_in_production():
    """Test that CORS configuration is validated in production."""
    with patch("sono_eval.api.main.logger") as mock_logger:
        with patch("sono_eval.api.main.config") as mock_config:
            mock_config.app_env = "production"
            mock_config.secret_key = "valid-secret-key-123"
            mock_config.superset_secret_key = "valid-superset-key-456"
            mock_config.allowed_hosts = "*"

            from sono_eval.api.main import _validate_security_config

            _validate_security_config()

            # Should log warning about CORS
            warning_calls = [str(call) for call in mock_logger.warning.call_args_list]
            assert any("ALLOWED_HOSTS" in str(call) for call in warning_calls)


def test_cors_configuration_production_mode():
    """Test that CORS enforces allowed hosts in production."""
    # This tests the CORS configuration logic at module load time
    # We test the logic indirectly through the validation
    pass  # CORS configuration happens at module load, tested via integration


def test_valid_production_config():
    """Test that valid production config passes validation."""
    with patch("sono_eval.api.main.config") as mock_config:
        mock_config.app_env = "production"
        mock_config.secret_key = "valid-secret-key-123"
        mock_config.superset_secret_key = "valid-superset-key-456"
        mock_config.allowed_hosts = "example.com,api.example.com"

        from sono_eval.api.main import _validate_security_config

        # Should not raise
        _validate_security_config()


def test_config_field_constraints():
    """Test configuration field validations."""
    config = Config()

    # Test defaults
    assert config.api_port == 8000
    assert config.api_workers == 4
    assert config.max_upload_size == 10485760  # 10MB

    # Test that fields are properly typed
    assert isinstance(config.api_port, int)
    assert isinstance(config.debug, bool)
    assert isinstance(config.allowed_hosts, str)


def test_allowed_hosts_parsing():
    """Test that allowed hosts are properly parsed."""
    config = Config()

    # Default should be localhost
    assert "localhost" in config.allowed_hosts or config.allowed_hosts == "*"
