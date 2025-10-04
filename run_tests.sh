#!/bin/bash

# Setup X11 display
export DISPLAY=:99

# Start D-Bus session
eval $(dbus-launch --sh-syntax)
export DBUS_SESSION_BUS_ADDRESS

# Wait a bit for D-Bus
sleep 1

# Start AT-SPI bus launcher in background
/usr/libexec/at-spi-bus-launcher --launch-immediately &
ATSPI_PID=$!

# Wait for AT-SPI to initialize
sleep 2

# Run the tests
python3 /app/test_linux_agent.py

# Cleanup
kill $ATSPI_PID 2>/dev/null || true
