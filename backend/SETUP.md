# Setup Instructions for Focus Tracker

## Installation

Due to network/SSL certificate issues in some environments, follow these steps:

### Option 1: Using Virtual Environment (Recommended)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies (use trusted-host flags to avoid SSL certificate issues)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Option 2: Using System Python (with --break-system-packages)

```bash
cd backend
pip install --break-system-packages -r requirements.txt
```

## Connecting to Your Camera

### Step 1: Test Camera Connection

First, test if your camera is detected:

```bash
# Find all available cameras
python test_camera.py

# Test a specific camera with live preview
python test_camera.py live 0
# (Try 0, 1, 2, etc. if 0 doesn't work)
```

### Step 2: Camera Permissions (macOS)

If you're on macOS, you may need to grant camera permissions:

1. Go to **System Preferences** > **Security & Privacy** > **Privacy** tab
2. Select **Camera** from the left sidebar
3. Make sure your terminal/IDE has camera access enabled
4. If you're using a virtual environment, you may need to grant permissions to the Python executable

### Step 3: Camera Index Configuration

By default, the application uses camera index `0`. If you have multiple cameras or camera index 0 doesn't work:

1. Run `python test_camera.py` to find available cameras
2. Edit `main.py` and change the `camera_index` parameter:
   ```python
   webcam = Webcam(camera_index=1, width=640, height=480)  # Change 0 to your camera index
   ```

## Running the Application

Once dependencies are installed and camera is connected:

```bash
# From the backend directory
python main.py

# Or if using virtual environment:
source venv/bin/activate
python main.py
```

## Testing

Run the test script to verify installation:

```bash
python test_imports.py
```

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate errors when installing packages:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org opencv-python mediapipe numpy
```

### Webcam Not Found

1. **Run the camera test script:**
   ```bash
   python test_camera.py
   ```
   This will help you find which camera index works.

2. **Check if camera is in use:**
   - Close other applications that might be using the camera (Zoom, Skype, FaceTime, etc.)
   - On macOS, check Activity Monitor for camera-using processes

3. **Try different camera indices:**
   - Edit `main.py` and change `camera_index=0` to `1`, `2`, etc.
   - Or run: `python test_camera.py live 1` to test different indices

4. **Camera permissions (macOS):**
   - System Preferences > Security & Privacy > Privacy > Camera
   - Enable camera access for Terminal or your IDE
   - If using venv, you may need to grant permissions to the Python executable

5. **USB camera issues:**
   - Try unplugging and reconnecting the USB camera
   - Try a different USB port
   - Check if the camera works in other applications (e.g., Photo Booth on macOS)

### Performance Issues

- Lower the resolution in `webcam.py` (width and height parameters)
- Adjust detection thresholds in `focus_engine.py` (EAR_THRESHOLD, HEAD_POSE_THRESHOLD, etc.)

## Requirements

- Python 3.8 or higher
- Webcam (built-in or USB)
- Good lighting conditions for face detection
