#!/usr/bin/env python3
"""
Test script to validate imports and basic structure of the focus tracker.
"""
import sys

def test_imports():
    """Test if all required packages are installed."""
    print("Testing imports...")
    print("-" * 50)
    
    # Test OpenCV
    try:
        import cv2
        print(f"✓ OpenCV installed (version: {cv2.__version__})")
    except ImportError as e:
        print(f"✗ OpenCV not installed: {e}")
        return False
    
    # Test MediaPipe
    try:
        import mediapipe as mp
        print(f"✓ MediaPipe installed (version: {mp.__version__})")
    except ImportError as e:
        print(f"✗ MediaPipe not installed: {e}")
        return False
    
    # Test NumPy
    try:
        import numpy as np
        print(f"✓ NumPy installed (version: {np.__version__})")
    except ImportError as e:
        print(f"✗ NumPy not installed: {e}")
        return False
    
    print("-" * 50)
    print("All required packages are installed!")
    return True

def test_module_imports():
    """Test if our custom modules can be imported."""
    print("\nTesting module imports...")
    print("-" * 50)
    
    try:
        from webcam import Webcam
        print("✓ webcam module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import webcam: {e}")
        return False
    
    try:
        from focus_engine import FocusEngine, FocusStatus
        print("✓ focus_engine module imported successfully")
        print(f"  FocusStatus enum values: {[s.value for s in FocusStatus]}")
    except Exception as e:
        print(f"✗ Failed to import focus_engine: {e}")
        return False
    
    print("-" * 50)
    print("All modules imported successfully!")
    return True

def test_webcam_initialization():
    """Test webcam initialization (may fail if no webcam available)."""
    print("\nTesting webcam initialization...")
    print("-" * 50)
    
    try:
        from webcam import Webcam
        webcam = Webcam(camera_index=0)
        if webcam.initialize():
            print("✓ Webcam initialized successfully")
            webcam.release()
            return True
        else:
            print("✗ Webcam initialization failed (no webcam available or in use)")
            return False
    except Exception as e:
        print(f"✗ Webcam test error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Focus Tracker - Import and Structure Test")
    print("=" * 50)
    
    # Test package imports
    packages_ok = test_imports()
    
    if packages_ok:
        # Test module imports
        modules_ok = test_module_imports()
        
        if modules_ok:
            # Test webcam (optional)
            test_webcam_initialization()
            
            print("\n" + "=" * 50)
            print("✓ All tests passed! Ready to run main.py")
            print("=" * 50)
            print("\nTo run the focus tracker:")
            print("  python main.py")
        else:
            print("\n" + "=" * 50)
            print("✗ Module import tests failed")
            print("=" * 50)
            sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("✗ Package installation required")
        print("=" * 50)
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nOr using a virtual environment:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print("  pip install -r requirements.txt")
        sys.exit(1)
