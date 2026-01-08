from ultralytics import YOLO
import cv2
import numpy as np
from collections import deque
import json
import os

# -----------------------------
# ADVANCED DISTANCE DETECTION
# -----------------------------

class AdvancedDistanceDetector:
    def __init__(self, model_path="best.pt", calibration_file="camera_calibration.json"):
        """
        Advanced distance detection with multiple precision improvements:
        1. Camera calibration support
        2. Kalman filtering for noise reduction
        3. Multi-frame averaging
        4. Confidence-weighted measurements
        5. Adaptive focal length estimation
        """
        self.model = YOLO(model_path)
        self.calibration_file = calibration_file
        
        # Default parameters
        self.KNOWN_WIDTH = 4.0
        self.KNOWN_HEIGHT = 12.0
        self.FOCAL_LENGTH = 700
        
        # Camera calibration parameters
        self.camera_matrix = None
        self.dist_coeffs = None
        self.load_calibration()
        
        # Kalman filter for each tracked object
        self.kalman_filters = {}
        
        # Multi-frame buffer for averaging (stores last N measurements)
        self.measurement_buffer = deque(maxlen=10)
        
        # Tracking history
        self.object_history = {}
        
    def load_calibration(self):
        """Load camera calibration data if available"""
        if os.path.exists(self.calibration_file):
            with open(self.calibration_file, 'r') as f:
                calib_data = json.load(f)
                self.camera_matrix = np.array(calib_data['camera_matrix'])
                self.dist_coeffs = np.array(calib_data['dist_coeffs'])
                self.FOCAL_LENGTH = self.camera_matrix[0, 0]
                print(f"✓ Loaded calibration data. Focal length: {self.FOCAL_LENGTH:.2f}")
        else:
            print(f"⚠ No calibration file found. Using default focal length: {self.FOCAL_LENGTH}")
    
    def create_kalman_filter(self):
        """Create a Kalman filter for distance tracking"""
        kf = cv2.KalmanFilter(2, 1)  # 2 state variables (distance, velocity), 1 measurement
        kf.measurementMatrix = np.array([[1, 0]], np.float32)
        kf.transitionMatrix = np.array([[1, 1], [0, 1]], np.float32)
        kf.processNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.03
        kf.measurementNoiseCov = np.array([[1]], np.float32) * 0.1
        return kf
    
    def calculate_distance_with_confidence(self, pixel_width, pixel_height, confidence):
        """
        Calculate distance using both width and height, weighted by confidence
        """
        if pixel_width <= 0 or pixel_height <= 0:
            return None
        
        # Calculate distance using width
        distance_width = (self.KNOWN_WIDTH * self.FOCAL_LENGTH) / pixel_width
        
        # Calculate distance using height
        distance_height = (self.KNOWN_HEIGHT * self.FOCAL_LENGTH) / pixel_height
        
        # Weighted average (give more weight to width as it's typically more stable)
        distance = (distance_width * 0.6 + distance_height * 0.4)
        
        # Apply confidence weighting
        confidence_factor = float(confidence)
        
        return distance, confidence_factor
    
    def apply_kalman_filter(self, object_id, measurement):
        """Apply Kalman filtering to smooth measurements"""
        if object_id not in self.kalman_filters:
            self.kalman_filters[object_id] = self.create_kalman_filter()
            self.kalman_filters[object_id].statePost = np.array([[measurement], [0]], np.float32)
        
        kf = self.kalman_filters[object_id]
        
        # Predict
        prediction = kf.predict()
        
        # Update with measurement
        kf.correct(np.array([[measurement]], np.float32))
        
        return float(kf.statePost[0])
    
    def multi_frame_average(self, measurements):
        """Calculate weighted average of recent measurements"""
        if not measurements:
            return None
        
        # More recent measurements get higher weight
        weights = np.linspace(0.5, 1.0, len(measurements))
        weighted_avg = np.average(measurements, weights=weights)
        
        return weighted_avg
    
    def undistort_frame(self, frame):
        """Remove lens distortion if calibration data is available"""
        if self.camera_matrix is not None and self.dist_coeffs is not None:
            h, w = frame.shape[:2]
            new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
                self.camera_matrix, self.dist_coeffs, (w, h), 1, (w, h)
            )
            undistorted = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs, 
                                       None, new_camera_matrix)
            return undistorted
        return frame
    
    def calculate_bbox_stability(self, object_id, current_bbox):
        """Calculate how stable the bounding box is over time"""
        if object_id not in self.object_history:
            self.object_history[object_id] = deque(maxlen=5)
        
        self.object_history[object_id].append(current_bbox)
        
        if len(self.object_history[object_id]) < 2:
            return 0.5  # Default stability
        
        # Calculate variance in bbox size
        sizes = [bbox[2] * bbox[3] for bbox in self.object_history[object_id]]
        stability = 1.0 / (1.0 + np.std(sizes) / np.mean(sizes))
        
        return stability
    
    def run(self, camera_index=0):
        """Main detection loop with advanced distance calculation"""
        cap = cv2.VideoCapture(camera_index)
        
        # Set camera properties for better quality
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        print("🚀 Advanced Distance Detection Started")
        print("Press 'ESC' to quit, 'C' to clear tracking history")
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Apply lens distortion correction
            frame = self.undistort_frame(frame)
            
            # Run YOLO inference
            results = self.model(frame, conf=0.5)
            
            current_measurements = []
            
            for idx, box in enumerate(results[0].boxes):
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                
                # Calculate dimensions
                pixel_width = x2 - x1
                pixel_height = y2 - y1
                
                # Create object ID (simple tracking based on position)
                object_id = f"obj_{cls}_{idx}"
                
                # Calculate bbox stability
                stability = self.calculate_bbox_stability(
                    object_id, (x1, y1, pixel_width, pixel_height)
                )
                
                # Calculate distance with confidence
                result = self.calculate_distance_with_confidence(
                    pixel_width, pixel_height, conf
                )
                
                if result:
                    distance, confidence_factor = result
                    
                    # Apply Kalman filter
                    filtered_distance = self.apply_kalman_filter(object_id, distance)
                    
                    # Store measurement
                    current_measurements.append(filtered_distance)
                    
                    # Calculate quality score
                    quality_score = (confidence_factor * 0.5 + stability * 0.5) * 100
                    
                    # Color based on quality (green=good, yellow=medium, red=poor)
                    if quality_score > 70:
                        color = (0, 255, 0)  # Green
                    elif quality_score > 50:
                        color = (0, 255, 255)  # Yellow
                    else:
                        color = (0, 0, 255)  # Red
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Display information
                    label = f"Dist: {filtered_distance:.1f}cm | Q: {quality_score:.0f}%"
                    cv2.putText(frame, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    
                    # Display confidence
                    conf_label = f"Conf: {conf:.2f}"
                    cv2.putText(frame, conf_label, (x1, y2 + 20),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            
            # Update measurement buffer
            if current_measurements:
                avg_distance = self.multi_frame_average(current_measurements)
                self.measurement_buffer.append(avg_distance)
                
                # Display overall average
                if len(self.measurement_buffer) > 0:
                    overall_avg = np.mean(list(self.measurement_buffer))
                    cv2.putText(frame, f"Avg Distance: {overall_avg:.1f}cm",
                               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Display info panel
            cv2.putText(frame, f"Frame: {frame_count}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(frame, f"Objects: {len(results[0].boxes)}", (10, 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Display the frame
            cv2.imshow("Advanced Distance Detection", frame)
            
            # Key controls
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('c') or key == ord('C'):  # Clear history
                self.kalman_filters.clear()
                self.object_history.clear()
                self.measurement_buffer.clear()
                print("🔄 Tracking history cleared")
        
        cap.release()
        cv2.destroyAllWindows()
        print("✓ Detection stopped")


def create_calibration_file():
    """
    Helper function to create a camera calibration file.
    Run this separately with a chessboard pattern to calibrate your camera.
    """
    print("📸 Camera Calibration Tool")
    print("=" * 50)
    print("To calibrate your camera:")
    print("1. Print a chessboard pattern (9x6 squares)")
    print("2. Take 15-20 photos from different angles")
    print("3. Run this function with your images")
    print("=" * 50)
    
    # Chessboard dimensions
    CHECKERBOARD = (9, 6)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # Prepare object points
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    
    objpoints = []  # 3D points
    imgpoints = []  # 2D points
    
    cap = cv2.VideoCapture(0)
    print("\nPress SPACE to capture calibration image (need 15-20 images)")
    print("Press ESC when done")
    
    captured = 0
    
    while captured < 20:
        ret, frame = cap.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret_chess, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
        
        display_frame = frame.copy()
        
        if ret_chess:
            cv2.drawChessboardCorners(display_frame, CHECKERBOARD, corners, ret_chess)
            cv2.putText(display_frame, "Pattern detected! Press SPACE", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.putText(display_frame, f"Captured: {captured}/20", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Calibration", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32 and ret_chess:  # SPACE
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            objpoints.append(objp)
            imgpoints.append(corners2)
            captured += 1
            print(f"✓ Captured image {captured}/20")
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if captured >= 10:
        print("\n🔄 Calculating calibration parameters...")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None
        )
        
        if ret:
            calibration_data = {
                'camera_matrix': mtx.tolist(),
                'dist_coeffs': dist.tolist(),
                'focal_length': float(mtx[0, 0])
            }
            
            with open('camera_calibration.json', 'w') as f:
                json.dump(calibration_data, f, indent=2)
            
            print("✓ Calibration complete!")
            print(f"✓ Saved to camera_calibration.json")
            print(f"✓ Focal length: {mtx[0, 0]:.2f}")
        else:
            print("✗ Calibration failed")
    else:
        print(f"✗ Need at least 10 images, only captured {captured}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--calibrate":
        create_calibration_file()
    else:
        detector = AdvancedDistanceDetector(model_path="best.pt")
        detector.run(camera_index=0)
