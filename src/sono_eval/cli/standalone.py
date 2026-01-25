"""
Standalone entry point for Sono-Eval.

This module sets up the environment for running Sono-Eval as a standalone
executable (e.g., via PyInstaller) without a Docker container or .env file.
"""

import os
import sys
from pathlib import Path


def setup_standalone_env():
    """
    Configure environment variables for standalone execution.

    Sets defaults to use local filesystem storage and SQLite instead of
    Dockerized services (Postgres, Redis).
    """
    # Get the directory where the executable is running (or script location)
    if getattr(sys, "frozen", False):
        # We are running in a PyInstaller bundle
        base_dir = Path(sys.executable).parent
    else:
        # We are running as a normal script
        base_dir = Path.cwd()

    data_dir = base_dir / "sono_eval_data"
    data_dir.mkdir(parents=True, exist_ok=True)

    storage_path = data_dir / "memory"
    models_path = data_dir / "models"
    tagstudio_path = data_dir / "tagstudio"

    # Set environment variables if they aren't already set
    defaults = {
        "APP_NAME": "sono-eval-standalone",
        "APP_ENV": "production",  # Use production settings (but with local overrides)
        "DEBUG": "false",
        "LOG_LEVEL": "INFO",
        # Database: Use local SQLite
        "DATABASE_URL": f"sqlite:///{base_dir}/sono_eval.db",
        # Redis: Disable or point to localhost (code handles connection failure gracefully)
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        # Storage Paths
        "MEMU_STORAGE_PATH": str(storage_path),
        "T5_CACHE_DIR": str(models_path),
        "TAGSTUDIO_ROOT": str(tagstudio_path),
        # Feature Flags
        "ASSESSMENT_ENABLE_EXPLANATIONS": "true",
        "ASSESSMENT_MULTI_PATH_TRACKING": "true",
        "DARK_HORSE_MODE": "enabled",
        # Security (Auto-generated for local standalone use if not set)
        "SECRET_KEY": "standalone-local-key-do-not-use-in-cloud-production",
        "ALLOWED_HOSTS": "*",
    }

    for key, value in defaults.items():
        if key not in os.environ:
            os.environ[key] = value

    # Create directories
    storage_path.mkdir(parents=True, exist_ok=True)
    models_path.mkdir(parents=True, exist_ok=True)
    tagstudio_path.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    setup_standalone_env()

    # Initialize session manager for exit confirmation
    try:
        from sono_eval.cli.session_manager import get_session

        session = get_session()
    except Exception as e:
        # Session manager is optional - continue if it fails
        # Session manager is optional - continue if it fails

        if hasattr(sys, "_getframe"):
            print(
                f"Warning: Could not initialize session manager: {e}", file=sys.stderr
            )

    # Import main CLI after setting up environment
    from sono_eval.cli.main import cli

    # Check if arguments were provided
    if len(sys.argv) == 1:
        # No arguments provided, launch interactive guidance
        print("\n\033[1;34m=== Sono-Eval Standalone ===\033[0m")
        print("Running in interactive mode...\n")

        try:
            from sono_eval.cli.onboarding import run_interactive_setup

            run_interactive_setup()

            # After setup, offer to run an assessment
            print("\n\033[1;36mWould you like to run a demo assessment now?\033[0m")
            response = input("Run demo (y/n)? [y]: ").strip().lower()
            if response in ("", "y", "yes"):
                print("\nRunning demo assessment...")
                # Synthesize arguments for the CLI
                sys.argv = [
                    sys.argv[0],
                    "assess",
                    "run",
                    "--candidate-id",
                    "demo-user",
                    "--content",
                    "def hello(): pass",
                    "--paths",
                    "technical",
                ]
                cli()
            else:
                print("\nUse './sono-eval --help' to see all available commands.")
                from sono_eval.cli.session_manager import end_current_session

                end_current_session()
                sys.exit(0)

        except ImportError:
            # Fallback if onboarding module implies complex depends
            print("To see available commands, run with --help")
            cli()
        except KeyboardInterrupt:
            # Exit confirmation is handled by SessionManager signal handler
            print("\nExiting.")
            from sono_eval.cli.session_manager import end_current_session

            end_current_session()
            sys.exit(0)
        except Exception as e:
            # If interactive mode fails, fall back to CLI help
            print(f"Interactive mode error: {e}")
            cli()
    else:
        # Arguments provided, run as normal CLI
        cli()
