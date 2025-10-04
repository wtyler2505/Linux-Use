#!/bin/bash

# Script to run TUI integration tests

set -e

echo "======================================"
echo "Linux-Use TUI Integration Tests"
echo "======================================"

# Setup display if not set
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY not set, starting Xvfb..."
    Xvfb :99 -screen 0 1920x1080x24 &
    XVFB_PID=$!
    export DISPLAY=:99
    sleep 2
    echo "✓ Xvfb running on :99"
fi

# Load environment
if [ -f "/app/.env" ]; then
    echo "Loading environment from .env..."
    export $(cat /app/.env | grep -v '^#' | xargs)
fi

# Run tests
echo ""
echo "Running tests..."
echo ""

cd /app
python tests/test_tui_integration.py

EXIT_CODE=$?

# Cleanup
if [ ! -z "$XVFB_PID" ]; then
    echo ""
    echo "Cleaning up Xvfb..."
    kill $XVFB_PID 2>/dev/null || true
fi

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed (exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE