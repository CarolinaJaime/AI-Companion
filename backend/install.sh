#!/bin/bash
# Installation script for focus tracker dependencies

cd "$(dirname "$0")"

echo "Installing Focus Tracker Dependencies"
echo "======================================"
echo ""

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
    echo "✓ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org > /dev/null 2>&1

# Install requirements
echo "Installing packages (this may take a few minutes)..."
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✓ Installation completed successfully!"
    echo "======================================"
    echo ""
    echo "To run the application:"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
    echo "Or use the run script:"
    echo "  ./run.sh"
else
    echo ""
    echo "======================================"
    echo "✗ Installation failed"
    echo "======================================"
    exit 1
fi
