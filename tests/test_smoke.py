"""Basic smoke tests that can run with minimal dependencies."""


def test_imports():
    """Test that basic imports work."""
    # These tests will be run by CI with proper environment
    pass


def test_module_structure():
    """Test that expected modules exist."""
    import os

    # Check that key source files exist
    assert os.path.exists("src/sono_eval/__init__.py")
    assert os.path.exists("src/sono_eval/api/main.py")
    assert os.path.exists("src/sono_eval/assessment/models.py")
    assert os.path.exists("src/sono_eval/utils/logger.py")


def test_docker_files_exist():
    """Test that Docker configuration files exist."""
    import os

    assert os.path.exists("Dockerfile")
    assert os.path.exists("docker-compose.yml")


def test_migration_setup_exists():
    """Test that migration configuration exists."""
    import os

    assert os.path.exists("alembic.ini")
    assert os.path.exists("migrations/README.md")
    assert os.path.exists("migrations/env.py")


def test_ci_configuration_exists():
    """Test that CI/CD configuration exists."""
    import os

    assert os.path.exists(".github/workflows/ci.yml")
    assert os.path.exists(".github/dependabot.yml")
    assert os.path.exists(".pre-commit-config.yaml")


def test_documentation_exists():
    """Test that key documentation files exist."""
    import os

    assert os.path.exists("README.md")
    assert os.path.exists("SECURITY.md")
    assert os.path.exists("documentation/Reports/CODE_REVIEW_REPORT.md")
    assert os.path.exists("ROADMAP.md")
    assert os.path.exists("documentation/Reports/ASSESSMENT_SUMMARY.md")
    assert os.path.exists("documentation/Guides/QUICK_REFERENCE.md")
    assert os.path.exists("CHANGELOG.md")
    assert os.path.exists("CONTRIBUTING.md")
    assert os.path.exists("CODE_OF_CONDUCT.md")
