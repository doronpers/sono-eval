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

# Apply the fix using a temporary file (works on both macOS and Linux)
TEMP_FILE=$(mktemp)

while IFS= read -r line; do
    echo "$line"
    # Check if we're at the line that starts with "if [ -x "$INSTALL_PYTHON" ]; then"
    # shellcheck disable=SC2016
    if echo "$line" | grep -q '^if \[ -x "\$INSTALL_PYTHON" \]; then$' || \
       echo "$line" | grep -q '^if \[ -x "$INSTALL_PYTHON" ]; then$'; then
        # Add the SSL certificate fix
        echo "    # Set SSL certificate path for Python 3.13 to fix certificate verification issues"
        echo "    CERT_FILE=\$(\"$INSTALL_PYTHON\" -c \"import certifi; print(certifi.where())\" 2>/dev/null || echo \"/opt/homebrew/etc/openssl@3/cert.pem\")"
        echo "    if [ -f \"\$CERT_FILE\" ]; then"
        echo "        export SSL_CERT_FILE=\"\$CERT_FILE\""
        echo "    fi"
    fi
done < "$HOOK_FILE" > "$TEMP_FILE"

mv "$TEMP_FILE" "$HOOK_FILE"
chmod +x "$HOOK_FILE"

echo "SSL certificate fix applied successfully to pre-commit hook"
echo "Certificate file: $CERT_FILE"
