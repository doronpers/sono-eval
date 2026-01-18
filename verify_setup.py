#!/usr/bin/env python3
"""
Setup verification script for Sono-Eval.
Checks all prerequisites and configuration.
"""

import sys
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (required: 3.9+)")
        print(f"   💡 This version supports all Sono-Eval features")
        print(f"   📚 Why this matters: Python 3.9+ enables modern features and better performance")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (required: 3.9+)")
        print(f"   💡 Update Python to access all features: https://www.python.org/downloads/")
        print(f"   📚 Why this matters: Newer Python versions provide better security and performance")
        return False


def check_dependencies():
    """Check if critical dependencies are installed."""
    critical = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("pydantic", "Data validation"),
        ("click", "CLI framework"),
        ("jinja2", "Template engine"),
    ]

    missing = []
    for module, desc in critical:
        try:
            __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"❌ {module} - {desc} (MISSING)")
            print(f"   💡 Install with: pip install {module}")
            print(f"   📚 Why this matters: {desc} is essential for Sono-Eval to function properly")
            missing.append(module)

    return len(missing) == 0


def check_optional_dependencies():
    """Check optional dependencies."""
    optional = [
        ("torch", "PyTorch (for ML models)"),
        ("transformers", "Hugging Face transformers"),
        ("redis", "Redis client"),
        ("sqlalchemy", "Database ORM"),
    ]

    for module, desc in optional:
        try:
            __import__(module)
            print(f"✅ {module} - {desc}")
        except ImportError:
            print(f"⚠️  {module} - {desc} (optional, not installed)")


def check_env_file():
    """Check if .env file exists."""
    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print(f"✅ .env file exists")
        return True
    elif env_example.exists():
        print(f"⚠️  .env file missing (but .env.example exists)")
        print(f"   Run: cp .env.example .env")
        return False
    else:
        print(f"❌ .env file missing (and no .env.example found)")
        return False


def check_data_directories():
    """Check if data directories exist or can be created."""
    dirs = [
        Path("./data/memory"),
        Path("./data/tagstudio"),
        Path("./models/cache"),
    ]

    all_ok = True
    for dir_path in dirs:
        if dir_path.exists():
            print(f"✅ {dir_path} exists")
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {dir_path} created")
            except Exception as e:
                print(f"❌ {dir_path} cannot be created: {e}")
                all_ok = False

    return all_ok


def check_package_installation():
    """Check if sono-eval package is installed."""
    try:
        import sono_eval

        print(f"✅ sono-eval package installed")
        return True
    except ImportError:
        print(f"⚠️  sono-eval package not installed")
        print(f"   Run: pip install -e .")
        return False


def check_docker():
    """Check if Docker is available."""
    import subprocess

    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Docker available: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(f"⚠️  Docker not available (optional, but recommended)")
    return False


def main():
    """Run all checks."""
    print("=" * 70)
    print("SONO-EVAL SETUP VERIFICATION")
    print("=" * 70)
    print()

    checks = {
        "Python Version": check_python_version(),
        "Critical Dependencies": check_dependencies(),
        "Package Installation": check_package_installation(),
        "Environment File": check_env_file(),
        "Data Directories": check_data_directories(),
    }

    print()
    print("Optional Components:")
    check_optional_dependencies()
    check_docker()

    print()
    print("=" * 70)

    failed = [name for name, passed in checks.items() if not passed]

    if not failed:
        print("✅ ALL CRITICAL CHECKS PASSED")
        print()
        print("🎉 You're ready to start using Sono-Eval!")
        print()
        print("📚 What you've accomplished:")
        print("  • Your environment is properly configured")
        print("  • All required components are installed")
        print("  • You're ready for your first assessment")
        print()
        print("Next steps:")
        print("  • Start the server: [cyan]sono-eval server start[/cyan]")
        print("  • Or use Docker: [cyan]./launcher.sh start[/cyan]")
        print("  • Then visit: [cyan]http://localhost:8000/mobile[/cyan]")
        print()
        print("💡 Tip: Use [cyan]sono-eval setup interactive[/cyan] for guided setup")
        print("💡 Or visit [cyan]http://localhost:8000/mobile/setup[/cyan] for web-based setup")
        return 0
    else:
        print(f"❌ {len(failed)} CRITICAL CHECK(S) FAILED:")
        for name in failed:
            print(f"   - {name}")
        print()
        print("💡 What this means:")
        print("   These checks ensure Sono-Eval can run properly on your system.")
        print("   Fix the issues above, then run this script again.")
        print()
        print("Need help? See: Documentation/Guides/resources/first-time-setup.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
