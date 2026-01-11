# How to Run the Focus Tracker

## ✅ Packages are Now Installed!

All required packages (OpenCV, MediaPipe, NumPy) have been installed in the virtual environment.

## Running the Application

### Option 1: Use the Run Script (Easiest)

```bash
cd backend
./run.sh
```

### Option 2: Manual Activation

```bash
cd backend
source venv/bin/activate
python main.py
```

### Option 3: Direct Python Command

```bash
cd backend
venv/bin/python main.py
```

## Important: Camera Permissions (macOS)

**You may see a camera permission error when running the application.** Here's how to fix it:

### Grant Camera Access to Terminal

1. **Open System Preferences** (or System Settings on macOS Ventura+)
2. Go to **Security & Privacy** > **Privacy** tab
3. Select **Camera** from the left sidebar
4. **Check the box** next to "Terminal" (or your terminal app like iTerm2)
5. If Terminal is not in the list, you may need to run the app once first to trigger the permission request

### Alternative: Grant Permissions via Command Line

```bash
# Reset camera permissions (requires restart of terminal)
tccutil reset Camera

# Then run your application - macOS will prompt for permission
```

### After Granting Permissions

1. **Close and reopen your terminal**
2. Run the application again:
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

## Testing Camera Connection

Before running the full application, test your camera:

```bash
cd backend
source venv/bin/activate
python test_camera.py
```

This will:
- Find all available cameras
- Show you which camera index to use
- Test camera with live preview (use `python test_camera.py live 0`)

## Troubleshooting

### "ModuleNotFoundError: No module named 'cv2'"

**Solution:** Make sure you're using the virtual environment:
```bash
cd backend
source venv/bin/activate  # IMPORTANT: Activate venv first!
python main.py
```

### "Camera access has been denied"

**Solution:** Grant camera permissions (see Camera Permissions section above)

### "Could not initialize webcam"

**Possible causes:**
1. Camera is in use by another app (Zoom, FaceTime, etc.)
2. Camera permissions not granted
3. Wrong camera index

**Solutions:**
1. Close other apps using the camera
2. Check camera permissions
3. Run `python test_camera.py` to find the correct camera index
4. Edit `main.py` line 18 to change `camera_index=0` to your working index

### Application Runs but No Video Window Appears

- Check if you see any error messages in the terminal
- Make sure you have camera permissions
- Try running `python test_camera.py live 0` first to test camera independently

## Quick Start Summary

1. **Activate virtual environment:**
   ```bash
   cd backend
   source venv/bin/activate
   ```

2. **Grant camera permissions** (see Camera Permissions section above)

3. **Test camera:**
   ```bash
   python test_camera.py
   ```

4. **Run application:**
   ```bash
   python main.py
   ```

5. **Press 'q' to quit** when the application is running

## What the Application Does

Once running, the application will:
- ✅ Open your webcam feed
- ✅ Detect your face in real-time
- ✅ Track eye movement (EAR - Eye Aspect Ratio)
- ✅ Monitor head pose (yaw, pitch angles)
- ✅ Analyze movement patterns
- ✅ Display your focus status:
  - 🟢 **FOCUSED** (green) - Eyes open, facing forward
  - 🟠 **DISTRACTED** (orange) - Eyes closed, looking away, or excessive movement
  - 🔴 **AWAY** (red) - No face detected

Enjoy your focus tracking! 🎯
