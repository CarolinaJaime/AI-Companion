#!/bin/bash
# Run script for focus tracker

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Current directory: $(pwd)"
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Virtual environment activated: $(which python)"
    echo ""
    # Use python from venv
    python main.py
else
    echo "ERROR: Virtual environment not found!"
    echo "Current directory: $(pwd)"
    echo "Looking for: venv/bin/activate"
    echo ""
    echo "Please install dependencies first:"
    echo "  cd /Users/fionaluo/AI-Companion/backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt"
    exit 1
fi
