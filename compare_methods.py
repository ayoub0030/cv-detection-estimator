from ultralytics import YOLO
import cv2
import numpy as np
import time
from collections import deque

# --------------------------------
# DISTANCE METHODS COMPARISON
# --------------------------------

class DistanceComparison:
    def __init__(self, model_path="best.pt"):
        """Compare all three distance calculation methods side-by-side"""
        self.model = YOLO(model_path)
        
        # Parameters
        self.KNOWN_WIDTH = 4.0
        self.KNOWN_HEIGHT = 12.0
        self.FOCAL_LENGTH = 700
        
        # Method 1: Basic smoothing
        self.smooth_distance_basic = 0
        
        # Method 2: Kalman filter
        self.kalman_filter = self.create_kalman_filter()
        
        # Method 3: Multi-frame buffer
        self.measurement_buffer = deque(maxlen=10)
        
        # Performance tracking
        self.fps_counter = deque(maxlen=30)
        self.method_times = {'basic': [], 'kalman': [], 'buffered': []}
        
    def create_kalman_filter(self):
        """Create Kalman filter for distance tracking"""
        kf = cv2.KalmanFilter(2, 1)
        kf.measurementMatrix = np.array([[1, 0]], np.float32)
        kf.transitionMatrix = np.array([[1, 1], [0, 1]], np.float32)
        kf.processNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.03
        kf.measurementNoiseCov = np.array([[1]], np.float32) * 0.1
        return kf
    
    def method_basic(self, pixel_width):
        """Method 1: Basic smoothing (from distanceWebcam.py)"""
        start_time = time.time()
        
        if pixel_width > 0:
            distance = (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / pixel_width
            
            if self.smooth_distance_basic == 0:
                self.smooth_distance_basic = distance
            else:
                self.smooth_distance_basic = (self.smooth_distance_basic * 0.9) + (distance * 0.1)
            
            result = self.smooth_distance_basic
        else:
            result = None
        
        self.method_times['basic'].append(time.time() - start_time)
        return result
    
    def method_kalman(self, pixel_width):
        """Method 2: Kalman filtering (from advanced_distance_detection.py)"""
        start_time = time.time()
        
        if pixel_width > 0:
            distance = (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / pixel_width
            
            # Predict
            self.kalman_filter.predict()
            
            # Update with measurement
            self.kalman_filter.correct(np.array([[distance]], np.float32))
            
            result = float(self.kalman_filter.statePost[0])
        else:
            result = None
        
        self.method_times['kalman'].append(time.time() - start_time)
        return result
    
    def method_buffered(self, pixel_width):
        """Method 3: Multi-frame averaging"""
        start_time = time.time()
        
        if pixel_width > 0:
            distance = (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / pixel_width
            self.measurement_buffer.append(distance)
            
            # Weighted average (recent measurements get higher weight)
            if len(self.measurement_buffer) > 0:
                weights = np.linspace(0.5, 1.0, len(self.measurement_buffer))
                result = np.average(list(self.measurement_buffer), weights=weights)
            else:
                result = distance
        else:
            result = None
        
        self.method_times['buffered'].append(time.time() - start_time)
        return result
    
    def calculate_statistics(self):
        """Calculate performance statistics"""
        stats = {}
        for method, times in self.method_times.items():
            if times:
                stats[method] = {
                    'avg_time': np.mean(times[-100:]) * 1000,  # Convert to ms
                    'std_dev': np.std(times[-100:]) * 1000
                }
        return stats
    
    def draw_comparison_panel(self, frame, distances, stats):
        """Draw side-by-side comparison panel"""
        panel_height = 200
        panel = np.zeros((panel_height, frame.shape[1], 3), dtype=np.uint8)
        
        # Title
        cv2.putText(panel, "Distance Methods Comparison", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Method results
        y_offset = 70
        methods = [
            ('Basic Smoothing', distances['basic'], (0, 255, 0)),
            ('Kalman Filter', distances['kalman'], (255, 255, 0)),
            ('Multi-Frame Buffer', distances['buffered'], (0, 255, 255))
        ]
        
        for i, (name, dist, color) in enumerate(methods):
            x_offset = 10 + (i * 400)
            
            # Method name
            cv2.putText(panel, name, (x_offset, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Distance value
            if dist is not None:
                cv2.putText(panel, f"{dist:.1f} cm", (x_offset, y_offset + 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            else:
                cv2.putText(panel, "N/A", (x_offset, y_offset + 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2)
            
            # Performance stats
            method_key = list(self.method_times.keys())[i]
            if method_key in stats:
                perf_text = f"{stats[method_key]['avg_time']:.2f}ms"
                cv2.putText(panel, perf_text, (x_offset, y_offset + 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # FPS
        if self.fps_counter:
            fps = len(self.fps_counter) / sum(self.fps_counter)
            cv2.putText(panel, f"FPS: {fps:.1f}", (10, panel_height - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return panel
    
    def run(self, camera_index=0):
        """Run comparison demo"""
        cap = cv2.VideoCapture(camera_index)
        
        print("=" * 60)
        print("🔍 Distance Detection Methods Comparison")
        print("=" * 60)
        print("This demo compares three distance calculation approaches:")
        print("  1. Basic Smoothing (green)")
        print("  2. Kalman Filter (yellow)")
        print("  3. Multi-Frame Buffer (cyan)")
        print()
        print("Press 'ESC' to quit, 'R' to reset filters")
        print("=" * 60)
        
        while True:
            frame_start = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break
            
            # Run YOLO detection
            results = self.model(frame, conf=0.5)
            
            distances = {'basic': None, 'kalman': None, 'buffered': None}
            
            # Process first detected object
            if len(results[0].boxes) > 0:
                box = results[0].boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                pixel_width = x2 - x1
                
                # Calculate distance using all three methods
                distances['basic'] = self.method_basic(pixel_width)
                distances['kalman'] = self.method_kalman(pixel_width)
                distances['buffered'] = self.method_buffered(pixel_width)
                
                # Draw bounding boxes with different colors
                colors = [(0, 255, 0), (255, 255, 0), (0, 255, 255)]
                for i, (method, dist) in enumerate(distances.items()):
                    if dist is not None:
                        offset = i * 3
                        cv2.rectangle(frame, 
                                    (x1 + offset, y1 + offset), 
                                    (x2 + offset, y2 + offset), 
                                    colors[i], 2)
            
            # Calculate statistics
            stats = self.calculate_statistics()
            
            # Draw comparison panel
            panel = self.draw_comparison_panel(frame, distances, stats)
            
            # Combine frame and panel
            combined = np.vstack([frame, panel])
            
            # Display
            cv2.imshow("Distance Methods Comparison", combined)
            
            # Track FPS
            frame_time = time.time() - frame_start
            self.fps_counter.append(frame_time)
            
            # Key controls
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('r') or key == ord('R'):  # Reset
                self.smooth_distance_basic = 0
                self.kalman_filter = self.create_kalman_filter()
                self.measurement_buffer.clear()
                print("🔄 Filters reset")
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Print final statistics
        print("\n" + "=" * 60)
        print("📊 Final Performance Statistics")
        print("=" * 60)
        stats = self.calculate_statistics()
        for method, data in stats.items():
            print(f"{method.upper():15} | Avg: {data['avg_time']:.3f}ms | StdDev: {data['std_dev']:.3f}ms")
        print("=" * 60)


if __name__ == "__main__":
    comparator = DistanceComparison(model_path="best.pt")
    comparator.run(camera_index=0)
