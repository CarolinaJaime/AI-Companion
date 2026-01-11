#!/bin/bash
# Test camera and then run the application

cd "$(dirname "$0")"

echo "=========================================="
echo "Focus Tracker - Camera Test & Run"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then: pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt"
    exit 1
fi

# Test camera first
echo "Step 1: Testing camera..."
echo ""

python test_camera.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Step 2: Running focus tracker..."
    echo "=========================================="
    echo ""
    echo "Press 'q' to quit the application"
    echo ""
    
    python main.py
else
    echo ""
    echo "=========================================="
    echo "Camera test failed!"
    echo "=========================================="
    echo ""
    echo "Please:"
    echo "1. Grant camera permissions in System Preferences > Security & Privacy > Camera"
    echo "2. Enable access for Terminal"
    echo "3. Close and reopen terminal"
    echo "4. Run this script again"
    exit 1
fi
