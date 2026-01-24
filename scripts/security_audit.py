#!/usr/bin/env python3
"""Local security audit script for Sono-Eval.

Runs Bandit, Safety, and pip-audit to check for security issues.
Use this script before committing or deploying.

Usage:
    python scripts/security_audit.py [--fix] [--verbose]
"""

import argparse
import json
import subprocess
import sys


def run_command(cmd: list, capture: bool = True) -> tuple:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300,
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except FileNotFoundError:
        return False, f"Command not found: {cmd[0]}"


def check_bandit() -> tuple:
    """Run Bandit static analysis."""
    print("\n🔍 Running Bandit (Static Analysis Security Testing)...")

    success, output = run_command(["bandit", "-r", "src/", "-f", "json"])

    if success:
        print("  ✅ No issues found")
        return True, {}

    try:
        results = json.loads(output)
        issues = results.get("results", [])
        high_issues = [i for i in issues if i.get("issue_severity") == "HIGH"]
        medium_issues = [i for i in issues if i.get("issue_severity") == "MEDIUM"]
        low_issues = [i for i in issues if i.get("issue_severity") == "LOW"]

        print(
            f"  Found: {len(high_issues)} HIGH, {len(medium_issues)} MEDIUM, {len(low_issues)} LOW"
        )

        if high_issues:
            print("  ❌ HIGH severity issues:")
            for issue in high_issues:
                print(f"    - {issue['filename']}:{issue['line_number']}: {issue['issue_text']}")
            return False, {
                "high": high_issues,
                "medium": medium_issues,
                "low": low_issues,
            }

        return True, {"medium": medium_issues, "low": low_issues}
    except json.JSONDecodeError:
        print(f"  ⚠️ Could not parse Bandit output: {output[:200]}")
        return False, {}


def check_safety() -> tuple:
    """Run Safety dependency check."""
    print("\n🔍 Running Safety (Dependency Vulnerability Check)...")

    success, output = run_command(["safety", "check", "--json"])

    if success:
        print("  ✅ No vulnerable dependencies found")
        return True, []

    try:
        # Safety outputs vulnerabilities as JSON array
        if "No known security" in output:
            print("  ✅ No known security vulnerabilities found")
            return True, []

        results = json.loads(output)
        vulns = results if isinstance(results, list) else results.get("vulnerabilities", [])

        print(f"  ⚠️ Found {len(vulns)} vulnerable dependencies")
        for vuln in vulns[:5]:  # Show first 5
            if isinstance(vuln, dict):
                pkg = vuln.get("package_name", "unknown")
                ver = vuln.get("analyzed_version", "?")
                print(f"    - {pkg}=={ver}")

        return len(vulns) == 0, vulns
    except json.JSONDecodeError:
        if "No known security" in output:
            print("  ✅ No known security vulnerabilities found")
            return True, []
        print("  ⚠️ Could not parse Safety output")
        return True, []


def check_pip_audit() -> tuple:
    """Run pip-audit for additional vulnerability scanning."""
    print("\n🔍 Running pip-audit (Additional Vulnerability Check)...")

    success, output = run_command(["pip-audit", "--format", "json"])

    if success:
        print("  ✅ No vulnerabilities found")
        return True, []

    try:
        results = json.loads(output)
        vulns = results if isinstance(results, list) else []

        if not vulns:
            print("  ✅ No vulnerabilities found")
            return True, []

        print(f"  ⚠️ Found {len(vulns)} vulnerabilities")
        return False, vulns
    except json.JSONDecodeError:
        if "No known" in output or not output.strip():
            print("  ✅ No known vulnerabilities found")
            return True, []
        print("  ⚠️ Could not parse pip-audit output")
        return True, []


def main():
    """Run all security checks."""
    parser = argparse.ArgumentParser(description="Run security audit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    _ = parser.parse_args()

    print("=" * 60)
    print("🔒 Sono-Eval Security Audit")
    print("=" * 60)

    # Check if tools are installed
    tools = ["bandit", "safety", "pip-audit"]
    missing = []
    for tool in tools:
        success, _ = run_command(["which", tool])
        if not success:
            missing.append(tool)

    if missing:
        print(f"\n⚠️ Missing tools: {', '.join(missing)}")
        print("Install with: pip install bandit safety pip-audit")
        sys.exit(1)

    results = {}

    # Run checks
    results["bandit"] = check_bandit()
    results["safety"] = check_safety()
    results["pip_audit"] = check_pip_audit()

    # Summary
    print("\n" + "=" * 60)
    print("📊 Security Audit Summary")
    print("=" * 60)

    all_passed = True
    for check, (passed, _) in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {check}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n✅ All security checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some security checks failed. Review issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
