#!/usr/bin/env python3
"""
Quick preview demo of Sono-Eval CLI and API capabilities.
This shows what the system looks like without requiring full dependencies.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def show_cli_structure():
    """Show the CLI command structure."""
    print("=" * 70)
    print("SONO-EVAL CLI COMMAND STRUCTURE")
    print("=" * 70)
    print()

    commands = {
        "sono-eval": {
            "description": "Main CLI entry point",
            "subcommands": {
                "assess": {
                    "description": "Assessment commands",
                    "commands": {"run": "Run an assessment with --candidate-id, --file, --paths"},
                },
                "candidate": {
                    "description": "Candidate management",
                    "commands": {
                        "create": "Create a new candidate",
                        "show": "Show candidate information",
                        "list": "List all candidates",
                        "delete": "Delete a candidate",
                    },
                },
                "tag": {
                    "description": "Tagging commands",
                    "commands": {"generate": "Generate semantic tags for code/text"},
                },
                "server": {
                    "description": "Server management",
                    "commands": {"start": "Start the API server (--host, --port, --reload)"},
                },
                "config": {
                    "description": "Configuration",
                    "commands": {"show": "Show current configuration"},
                },
            },
        }
    }

    def print_commands(cmd_dict, indent=0):
        for key, value in cmd_dict.items():
            prefix = "  " * indent
            if isinstance(value, dict):
                if "description" in value:
                    print(f"{prefix}{key}: {value['description']}")
                if "subcommands" in value:
                    print_commands(value["subcommands"], indent + 1)
                if "commands" in value:
                    print_commands(value["commands"], indent + 1)
            else:
                print(f"{prefix}  {key}: {value}")

    print_commands(commands)
    print()
    print("=" * 70)
    print("EXAMPLE USAGE")
    print("=" * 70)
    print()
    print("# Create a candidate")
    print("sono-eval candidate create --id candidate_001")
    print()
    print("# Run assessment")
    print("sono-eval assess run \\")
    print("  --candidate-id candidate_001 \\")
    print("  --file solution.py \\")
    print("  --paths technical design")
    print()
    print("# Generate tags")
    print("sono-eval tag generate --file mycode.js --max-tags 5")
    print()
    print("# Start API server")
    print("sono-eval server start --reload")
    print()


def show_api_endpoints():
    """Show the API endpoint structure."""
    print("=" * 70)
    print("SONO-EVAL REST API ENDPOINTS")
    print("=" * 70)
    print()

    endpoints = {
        "Health & Status": [
            ("GET", "/", "Root endpoint with API information"),
            ("GET", "/health", "Health check endpoint"),
            ("GET", "/status", "Detailed status information"),
        ],
        "Assessments": [
            ("POST", "/api/v1/assessments", "Create a new assessment"),
            ("GET", "/api/v1/assessments/{id}", "Get assessment by ID"),
        ],
        "Candidates": [
            ("POST", "/api/v1/candidates", "Create a new candidate"),
            ("GET", "/api/v1/candidates", "List all candidates"),
            ("GET", "/api/v1/candidates/{id}", "Get candidate memory"),
            ("DELETE", "/api/v1/candidates/{id}", "Delete a candidate"),
        ],
        "Tagging": [
            ("POST", "/api/v1/tags/generate", "Generate semantic tags"),
            ("POST", "/api/v1/files/upload", "Upload file for assessment"),
        ],
        "Mobile Interface": [
            ("GET", "/mobile/", "Mobile home page"),
            ("GET", "/mobile/start", "Start assessment page"),
            ("GET", "/mobile/paths", "Path selection page"),
            ("GET", "/mobile/assess", "Interactive assessment page"),
            ("GET", "/mobile/results", "Results page"),
            ("POST", "/api/mobile/assess", "Submit mobile assessment"),
            ("GET", "/api/mobile/explain/{path}", "Get path explanation"),
        ],
    }

    for category, items in endpoints.items():
        print(f"\n{category}:")
        for method, path, desc in items:
            method_color = {
                "GET": "\033[92m",
                "POST": "\033[94m",
                "DELETE": "\033[91m",
            }.get(method, "")
            reset = "\033[0m"
            print(f"  {method_color}{method:6}{reset} {path:35} - {desc}")

    print()
    print("=" * 70)
    print("API DOCUMENTATION")
    print("=" * 70)
    print()
    print("When the server is running, visit:")
    print("  • Interactive API Docs: http://localhost:8000/docs")
    print("  • Alternative Docs:     http://localhost:8000/redoc")
    print()


def show_mobile_features():
    """Show mobile interface features."""
    print("=" * 70)
    print("MOBILE COMPANION INTERFACE")
    print("=" * 70)
    print()
    print("Features:")
    print("  • Mobile-optimized responsive design")
    print("  • Interactive path selection")
    print("  • Real-time assessment feedback")
    print("  • Detailed explanations for each path")
    print("  • Progress tracking")
    print("  • Personalized recommendations")
    print()
    print("Access at: http://localhost:8000/mobile/")
    print()
    print("Assessment Paths:")
    paths = [
        ("⚙️", "Technical Skills", "Code quality, architecture, testing"),
        ("🎨", "Design Thinking", "Problem analysis, solution design"),
        ("🤝", "Collaboration", "Communication, teamwork, code review"),
        ("🧩", "Problem Solving", "Analytical thinking, debugging"),
    ]
    for icon, name, desc in paths:
        print(f"  {icon} {name:20} - {desc}")
    print()


def show_architecture():
    """Show system architecture overview."""
    print("=" * 70)
    print("SYSTEM ARCHITECTURE")
    print("=" * 70)
    print()
    print(
        """
    ┌─────────────────────────────────────────────────────────────┐
    │                     Sono-Eval System                        │
    ├─────────────────────────────────────────────────────────────┤
    │  Interfaces:  CLI  │  REST API  │  Mobile Web               │
    ├─────────────────────────────────────────────────────────────┤
    │  Core Engine:                                               │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
    │  │  Assessment  │  │   Semantic   │  │    Memory    │    │
    │  │    Engine    │  │    Tagging   │  │   (MemU)     │    │
    │  └──────────────┘  └──────────────┘  └──────────────┘    │
    ├─────────────────────────────────────────────────────────────┤
    │  Storage:  PostgreSQL  │  Redis  │  File System            │
    ├─────────────────────────────────────────────────────────────┤
    │  Analytics:  Apache Superset Dashboards                      │
    └─────────────────────────────────────────────────────────────┘
    """
    )


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SONO-EVAL PREVIEW")
    print("Explainable Multi-Path Developer Assessment System")
    print("=" * 70 + "\n")

    show_cli_structure()
    print("\n")
    show_api_endpoints()
    print("\n")
    show_mobile_features()
    print("\n")
    show_architecture()

    print("\n" + "=" * 70)
    print("TO RUN THE SYSTEM:")
    print("=" * 70)
    print()
    print("1. Using Docker (Recommended):")
    print("   ./launcher.sh start")
    print()
    print("2. Development Mode:")
    print("   ./launcher.sh dev")
    print("   source venv/bin/activate")
    print("   sono-eval server start")
    print()
    print("3. Access Points:")
    print("   • API Server:     http://localhost:8000")
    print("   • API Docs:       http://localhost:8000/docs")
    print("   • Mobile UI:      http://localhost:8000/mobile/")
    print("   • Superset:       http://localhost:8088 (admin/admin)")
    print()
    print("=" * 70 + "\n")
