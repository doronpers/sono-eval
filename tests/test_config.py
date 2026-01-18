"""Tests for the configuration system."""

import os

import pytest

from sono_eval.utils.config import Config, get_config


def test_config_defaults():
    """Test that config has sensible defaults."""
    config = Config()

    assert config.app_name == "sono-eval"
    assert config.api_port == 8000
    assert config.assessment_enable_explanations is True
    assert config.assessment_multi_path_tracking is True
    assert config.pattern_checks_enabled is True
    assert config.pattern_penalty_low > 0
    assert config.pattern_penalty_medium > config.pattern_penalty_low
    assert config.pattern_penalty_high > config.pattern_penalty_medium


def test_config_from_env(monkeypatch):
    """Test loading config from environment variables."""
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("DEBUG", "true")

    config = Config()

    assert config.api_port == 9000
    assert config.debug is True


def test_get_storage_path():
    """Test getting storage path."""
    config = Config()
    path = config.get_storage_path()

    assert path is not None
    assert path.exists()


def test_get_cache_dir():
    """Test getting cache directory."""
    config = Config()
    cache_dir = config.get_cache_dir()

    assert cache_dir is not None
    assert cache_dir.exists()


def test_get_tagstudio_root():
    """Test getting TagStudio root."""
    config = Config()
    root = config.get_tagstudio_root()

    assert root is not None
    assert root.exists()


def test_singleton_config():
    """Test that get_config returns singleton."""
    config1 = get_config()
    config2 = get_config()

    assert config1 is config2
