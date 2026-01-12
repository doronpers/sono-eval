#!/bin/bash
# Script to fix SSL certificate issues in pre-commit hooks
# Run this after: pre-commit install

HOOK_FILE=".git/hooks/pre-commit"

if [ ! -f "$HOOK_FILE" ]; then
    echo "Error: pre-commit hook not found at $HOOK_FILE"
    echo "Please run 'pre-commit install' first"
    exit 1
fi

# Find the Python executable used by pre-commit
INSTALL_PYTHON=$(grep "^INSTALL_PYTHON=" "$HOOK_FILE" | cut -d'=' -f2- | tr -d '"')

if [ -z "$INSTALL_PYTHON" ] || [ ! -x "$INSTALL_PYTHON" ]; then
    echo "Error: Could not find Python executable in pre-commit hook"
    exit 1
fi

# Get certificate file path
CERT_FILE=$("$INSTALL_PYTHON" -c "import certifi; print(certifi.where())" 2>/dev/null)

if [ -z "$CERT_FILE" ] || [ ! -f "$CERT_FILE" ]; then
    # Fallback to Homebrew certificates
    CERT_FILE="/opt/homebrew/etc/openssl@3/cert.pem"
    if [ ! -f "$CERT_FILE" ]; then
        echo "Error: Could not find SSL certificate file"
        exit 1
    fi
fi

# Check if fix is already applied
if grep -q "SSL_CERT_FILE" "$HOOK_FILE"; then
    echo "SSL certificate fix already applied to pre-commit hook"
    exit 0
fi

# Create backup
cp "$HOOK_FILE" "${HOOK_FILE}.bak"

# Apply the fix
sed -i.bak2 '/^if \[ -x "\$INSTALL_PYTHON" \]; then$/a\
    # Set SSL certificate path for Python 3.13 to fix certificate verification issues\
    CERT_FILE=$("$INSTALL_PYTHON" -c "import certifi; print(certifi.where())" 2>/dev/null || echo "/opt/homebrew/etc/openssl@3/cert.pem")\
    if [ -f "$CERT_FILE" ]; then\
        export SSL_CERT_FILE="$CERT_FILE"\
    fi
' "$HOOK_FILE"

# Clean up extra backup
rm -f "${HOOK_FILE}.bak2"

echo "SSL certificate fix applied successfully to pre-commit hook"
echo "Certificate file: $CERT_FILE"
