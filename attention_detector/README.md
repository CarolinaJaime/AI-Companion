# Attention Detector Desktop Application

A Python desktop application that uses OpenCV to detect when someone is paying attention to the computer versus when they are not, using live webcam feedback.

## Features

- **Real-time webcam feed** - Live video from your webcam
- **Face detection** - Detects faces in the video stream
- **Eye tracking** - Identifies when eyes are visible and detected
- **Attention scoring** - Calculates an attention percentage based on multiple factors:
  - Face detection (base score)
  - Face position (centered vs offset)
  - Eye visibility (both eyes detected)
  - Face size (optimal distance from camera)
- **Visual feedback** - Color-coded status indicators (green = attentive, red = not attentive)
- **Progress bar** - Visual representation of attention percentage

## Requirements

- Python 3.7 or higher
- Webcam/camera connected to your computer
- Windows/Linux/macOS

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install opencv-python numpy Pillow
```

## Usage

1. Run the application:
```bash
python attention_detector.py
```

2. The application will open with a window showing:
   - Live webcam feed
   - Status indicators
   - Control buttons

3. Click "Start Detection" to begin monitoring attention

4. Click "Stop Detection" to pause monitoring

## How It Works

The application uses OpenCV's Haar Cascade classifiers to:
1. Detect faces in each frame
2. Identify eye regions within detected faces
3. Calculate attention score based on:
   - Presence of a face (30 points)
   - Face centered horizontally (0-25 points)
   - Face centered vertically (0-20 points)
   - Eyes detected (0-25 points)
   - Optimal face size (0-10 points)

Total possible score: 110 points (normalized to 100%)
Attention threshold: 60% (configurable in code)

## Tips for Best Results

- Ensure good lighting in your environment
- Face the camera directly
- Keep your eyes visible (avoid wearing sunglasses)
- Maintain a comfortable distance from the camera (not too close or too far)
- Ensure the camera has permission to access your webcam

## Troubleshooting

**Webcam not working:**
- Check if the webcam is connected and not being used by another application
- Try changing the camera index in the code (currently set to 0)

**Detection not working:**
- Ensure adequate lighting
- Check if you're facing the camera directly
- Make sure your face and eyes are clearly visible

**Performance issues:**
- Lower the camera resolution in the code if needed
- Close other applications using the webcam

## License

This project is provided as-is for educational and personal use.
