# Scripts Directory

This directory contains utility scripts for the sono-eval project.

## fix-pre-commit-ssl.sh

Fixes SSL certificate verification issues with pre-commit hooks when using Python 3.13.

### Problem

When using Python 3.13 installed from python.org (not Homebrew), the pre-commit hooks may fail with SSL certificate verification errors when trying to install hooks like `markdownlint-cli`:

```
ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

This happens because Python 3.13 doesn't have SSL certificates configured by default.

### Solution

Run this script after installing pre-commit hooks:

```bash
pre-commit install
./scripts/fix-pre-commit-ssl.sh
```

The script will:

1. Detect the Python executable used by pre-commit
2. Find the SSL certificate file (using `certifi` package or Homebrew certificates)
3. Update the pre-commit hook to set the `SSL_CERT_FILE` environment variable

### When to Run

- After running `pre-commit install` for the first time
- After reinstalling pre-commit hooks
- If you encounter SSL certificate errors when committing

The script is idempotent - it's safe to run multiple times.
