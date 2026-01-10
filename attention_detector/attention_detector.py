import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time

class AttentionDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Attention Detector")
        self.root.geometry("800x600")
        
        # State variables
        self.running = False
        self.cap = None
        self.current_frame = None
        self.attention_status = "Unknown"
        self.attention_percentage = 0
        
        # Statistics tracking variables
        self.focused_seconds = 0.0
        self.distracted_seconds = 0.0
        self.total_detection_time = 0.0
        self.attention_percentages = []  # Store all attention percentages for averaging
        self.stats_thread = None
        self.last_print_time = 0
        self.detection_start_time = 0
        self.last_frame_time = 0
        
        # OpenCV classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        # Setup GUI
        self.setup_gui()
        
        # Start webcam
        self.start_camera()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left side: Video and status
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Video display
        self.video_label = ttk.Label(left_frame, text="Initializing camera...")
        self.video_label.grid(row=0, column=0, pady=10)
        
        # Status frame
        status_frame = ttk.LabelFrame(left_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Attention status label
        self.status_label = ttk.Label(status_frame, text="Status: Unknown", font=("Arial", 14, "bold"))
        self.status_label.grid(row=0, column=0, pady=5)
        
        # Attention percentage
        self.percentage_label = ttk.Label(status_frame, text="Attention: 0%", font=("Arial", 12))
        self.percentage_label.grid(row=1, column=0, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(status_frame, length=300, mode='determinate', maximum=100)
        self.progress_bar.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Instructions
        info_frame = ttk.LabelFrame(left_frame, text="Instructions", padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        info_text = "• Look directly at the camera for best detection\n"
        info_text += "• Face the camera and keep your eyes visible\n"
        info_text += "• Green indicator = Paying attention\n"
        info_text += "• Red indicator = Not paying attention"
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Right side: Control buttons
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Control buttons
        control_frame = ttk.LabelFrame(right_frame, text="Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E), pady=10)
        
        self.start_button = ttk.Button(control_frame, text="Start Detection", command=self.start_detection, width=20)
        self.start_button.grid(row=0, column=0, pady=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Detection", command=self.stop_detection, state=tk.DISABLED, width=20)
        self.stop_button.grid(row=1, column=0, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)
        
    def start_camera(self):
        """Initialize the webcam"""
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open webcam")
            # Set camera resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            self.video_label.config(text=f"Error: {str(e)}")
            
    def calculate_eye_aspect_ratio(self, eye):
        """Calculate Eye Aspect Ratio (EAR) for blink detection"""
        # Compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])
        
        # Compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = np.linalg.norm(eye[0] - eye[3])
        
        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_attention(self, frame):
        """Detect if person is paying attention"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return False, 0, frame  # No face detected
        
        # Get the largest face (assuming it's the main person)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        
        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Region of Interest for eyes
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes
        eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
        
        # Calculate attention metrics
        attention_score = 0
        eye_count = len(eyes)
        
        # Face position and size (center and size relative to frame)
        frame_height, frame_width = frame.shape[:2]
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        
        # Check if face is centered (within 30% of center)
        center_threshold = 0.3
        x_center_offset = abs(face_center_x - frame_width // 2) / (frame_width // 2)
        y_center_offset = abs(face_center_y - frame_height // 2) / (frame_height // 2)
        
        # Face size (should be reasonable, not too small or too large)
        face_area = w * h
        frame_area = frame_width * frame_height
        face_ratio = face_area / frame_area
        
        # Calculate attention based on multiple factors
        factors = {
            'face_detected': 30,  # Base score for having a face
            'face_centered_x': 0,
            'face_centered_y': 0,
            'eyes_detected': 0,
            'face_size': 0
        }
        
        # Face centered score (x-axis)
        if x_center_offset < center_threshold:
            factors['face_centered_x'] = 25
        elif x_center_offset < 0.5:
            factors['face_centered_x'] = 15
        
        # Face centered score (y-axis)
        if y_center_offset < center_threshold:
            factors['face_centered_y'] = 20
        elif y_center_offset < 0.5:
            factors['face_centered_y'] = 10
        
        # Eyes detected score
        if eye_count >= 2:
            factors['eyes_detected'] = 25
            # Draw eye rectangles
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        elif eye_count == 1:
            factors['eyes_detected'] = 10
        
        # Face size score (optimal size is around 10-30% of frame)
        if 0.05 < face_ratio < 0.40:
            factors['face_size'] = 10
        elif 0.02 < face_ratio < 0.50:
            factors['face_size'] = 5
        
        attention_score = sum(factors.values())
        
        # Determine if paying attention (threshold: 60%)
        is_attentive = attention_score >= 60
        
        return is_attentive, attention_score, frame
    
    def update_frame(self):
        """Continuously update the video frame"""
        while True:
            if self.cap is None or not self.cap.isOpened():
                break
                
            ret, frame = self.cap.read()
            if not ret:
                break
            
            if self.running:
                # Detect attention
                is_attentive, score, processed_frame = self.detect_attention(frame.copy())
                
                # Update status
                self.attention_status = "Paying Attention" if is_attentive else "Not Paying Attention"
                self.attention_percentage = min(100, max(0, int(score)))
                
                # Track time spent focused vs distracted
                current_time = time.time()
                if self.last_frame_time > 0:
                    time_delta = current_time - self.last_frame_time
                    if is_attentive:
                        self.focused_seconds += time_delta
                    else:
                        self.distracted_seconds += time_delta
                    self.total_detection_time += time_delta
                    
                    # Store attention percentage for averaging
                    self.attention_percentages.append(self.attention_percentage)
                
                self.last_frame_time = current_time
                
                # Add status text to frame
                color = (0, 255, 0) if is_attentive else (0, 0, 255)
                cv2.putText(processed_frame, self.attention_status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(processed_frame, f"Score: {self.attention_percentage}%", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                
                self.current_frame = processed_frame
            else:
                # Just show the raw frame with instructions
                cv2.putText(frame, "Press 'Start Detection' to begin", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                self.current_frame = frame
            
            # Convert to RGB for tkinter
            frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(image=frame_pil)
            
            # Update GUI in main thread
            self.root.after(0, self.update_gui, frame_tk)
            
            time.sleep(0.03)  # ~30 FPS
    
    def update_gui(self, frame_tk):
        """Update GUI elements (must be called from main thread)"""
        # Update video display
        self.video_label.config(image=frame_tk)
        self.video_label.image = frame_tk  # Keep a reference
        
        if self.running:
            # Update status
            color = "green" if self.attention_status == "Paying Attention" else "red"
            self.status_label.config(text=f"Status: {self.attention_status}", foreground=color)
            self.percentage_label.config(text=f"Attention: {self.attention_percentage}%")
            self.progress_bar['value'] = self.attention_percentage
    
    def print_stats_periodically(self):
        """Print attention statistics every 2 seconds"""
        while self.running:
            time.sleep(2)
            if self.running and self.attention_percentage >= 0:
                focused_mins = int(self.focused_seconds // 60)
                focused_secs = int(self.focused_seconds % 60)
                distracted_mins = int(self.distracted_seconds // 60)
                distracted_secs = int(self.distracted_seconds % 60)
                
                print(f"\n[{time.strftime('%H:%M:%S')}] Current Attention: {self.attention_percentage}% | "
                      f"Status: {self.attention_status}")
                print(f"  Time Focused: {focused_mins}m {focused_secs}s | "
                      f"Time Distracted: {distracted_mins}m {distracted_secs}s")
    
    def start_detection(self):
        """Start the attention detection"""
        if not self.running:
            # Reset statistics
            self.focused_seconds = 0.0
            self.distracted_seconds = 0.0
            self.total_detection_time = 0.0
            self.attention_percentages = []
            self.last_frame_time = 0
            self.detection_start_time = time.time()
            
            print("\n" + "="*60)
            print("ATTENTION DETECTION STARTED")
            print("="*60)
            print(f"Starting time: {time.strftime('%H:%M:%S')}\n")
            
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Start stats printing thread
            self.stats_thread = threading.Thread(target=self.print_stats_periodically, daemon=True)
            self.stats_thread.start()
    
    def stop_detection(self):
        """Stop the attention detection"""
        self.running = False
        
        # Calculate average statistics
        total_time = self.focused_seconds + self.distracted_seconds
        if total_time > 0:
            avg_attention = sum(self.attention_percentages) / len(self.attention_percentages) if self.attention_percentages else 0
            focused_percentage = (self.focused_seconds / total_time) * 100
            distracted_percentage = (self.distracted_seconds / total_time) * 100
            
            focused_mins = int(self.focused_seconds // 60)
            focused_secs = int(self.focused_seconds % 60)
            distracted_mins = int(self.distracted_seconds // 60)
            distracted_secs = int(self.distracted_seconds % 60)
            total_mins = int(total_time // 60)
            total_secs = int(total_time % 60)
            
            print("\n" + "="*60)
            print("ATTENTION DETECTION STOPPED")
            print("="*60)
            print(f"\n📊 AVERAGE STATISTICS:")
            print(f"  Average Attention Percentage: {avg_attention:.1f}%")
            print(f"\n⏱️  TIME BREAKDOWN:")
            print(f"  Total Detection Time: {total_mins}m {total_secs}s")
            print(f"  Time Focused: {focused_mins}m {focused_secs}s ({focused_percentage:.1f}%)")
            print(f"  Time Distracted: {distracted_mins}m {distracted_secs}s ({distracted_percentage:.1f}%)")
            print("="*60 + "\n")
        else:
            print("\n" + "="*60)
            print("ATTENTION DETECTION STOPPED")
            print("="*60)
            print("No data collected.\n")
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", foreground="black")
        self.percentage_label.config(text="Attention: 0%")
        self.progress_bar['value'] = 0
    
    def run(self):
        """Start the application"""
        # Start video update thread
        video_thread = threading.Thread(target=self.update_frame, daemon=True)
        video_thread.start()
        
        # Handle window closing
        def on_closing():
            self.running = False
            if self.cap is not None:
                self.cap.release()
            self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

def main():
    root = tk.Tk()
    app = AttentionDetector(root)
    app.run()

if __name__ == "__main__":
    main()
