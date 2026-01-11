#!/usr/bin/env python3
"""
Simple script to test camera connection and find available cameras.
"""
import cv2
import sys

def test_camera(camera_index: int, width: int = 640, height: int = 480):
    """
    Test if a camera is available at the given index.
    
    Args:
        camera_index: Camera device index
        width: Frame width
        height: Frame height
        
    Returns:
        True if camera works, False otherwise
    """
    print(f"Testing camera {camera_index}...")
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"  ✗ Camera {camera_index} is not available")
        return False
    
    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Try to read a frame
    ret, frame = cap.read()
    if not ret or frame is None:
        print(f"  ✗ Camera {camera_index} opened but cannot read frames")
        cap.release()
        return False
    
    # Get actual resolution
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"  ✓ Camera {camera_index} is working!")
    print(f"    Resolution: {actual_width}x{actual_height}")
    print(f"    FPS: {fps}")
    cap.release()
    return True

def find_available_cameras(max_cameras: int = 5):
    """
    Find all available cameras.
    
    Args:
        max_cameras: Maximum number of cameras to check
        
    Returns:
        List of working camera indices
    """
    print("=" * 60)
    print("Camera Detection Test")
    print("=" * 60)
    print()
    
    available_cameras = []
    
    for i in range(max_cameras):
        if test_camera(i):
            available_cameras.append(i)
        print()
    
    return available_cameras

def test_camera_live(camera_index: int = 0):
    """
    Test camera with live preview.
    
    Args:
        camera_index: Camera device index
    """
    print(f"Opening camera {camera_index} for live test...")
    print("Press 'q' to quit")
    print()
    
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print(f"ERROR: Could not open camera {camera_index}")
        print("Possible reasons:")
        print("  1. Camera is not connected")
        print("  2. Camera is in use by another application")
        print("  3. Camera permissions not granted (macOS)")
        print("  4. Wrong camera index - try running: python test_camera.py")
        sys.exit(1)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    frame_count = 0
    print("Camera is working! You should see a window with camera feed.")
    print()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame")
                break
            
            frame_count += 1
            
            # Display frame info
            info_text = f"Camera {camera_index} - Frame: {frame_count} - Press 'q' to quit"
            cv2.putText(frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            cv2.imshow('Camera Test', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\nCamera test completed. Processed {frame_count} frames.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "live":
            # Test with live preview
            camera_idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
            test_camera_live(camera_idx)
        else:
            # Test specific camera
            camera_idx = int(sys.argv[1])
            if test_camera(camera_idx):
                print(f"\n✓ Camera {camera_idx} is ready to use!")
                print(f"Update main.py to use camera_index={camera_idx}")
            else:
                print(f"\n✗ Camera {camera_idx} is not available")
                sys.exit(1)
    else:
        # Find all available cameras
        cameras = find_available_cameras()
        
        if cameras:
            print("=" * 60)
            print(f"Found {len(cameras)} available camera(s): {cameras}")
            print("=" * 60)
            print()
            print("To test a camera with live preview, run:")
            print(f"  python test_camera.py live {cameras[0]}")
            print()
            print("To use a specific camera in main.py, change:")
            print("  webcam = Webcam(camera_index=0, ...)")
            print(f"  to: webcam = Webcam(camera_index={cameras[0]}, ...)")
        else:
            print("=" * 60)
            print("✗ No cameras found!")
            print("=" * 60)
            print()
            print("Troubleshooting:")
            print("  1. Make sure your camera is connected")
            print("  2. On macOS: Check System Preferences > Security & Privacy > Camera")
            print("  3. Make sure no other application is using the camera")
            print("  4. Try disconnecting and reconnecting the camera")
            sys.exit(1)
