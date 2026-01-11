import cv2
import numpy as np
from ultralytics import YOLO

# --------------------------------
# DEPTH FUSION DETECTION
# --------------------------------

class DepthFusionDetector:
    def __init__(self, model_path="best.pt"):
        self.yolo_model = YOLO(model_path)
        
        # Load MiDaS depth estimation model
        self.depth_model = cv2.dnn.readNet(
            "_depth_small.onnx"  # Lightweight depth model
        )
        
        # Aruco marker parameters
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()
        
        # Reference marker (5cm x 5cm)
        self.MARKER_SIZE = 5.0
        
        # Hybrid weights (geometric vs depth model)
        self.geometric_weight = 0.7
        self.depth_weight = 0.3

    def detect_reference_markers(self, frame):
        """Detect Aruco markers for real-world scaling"""
        corners, ids, _ = cv2.aruco.detectMarkers(
            frame, self.aruco_dict, parameters=self.aruco_params
        )
        
        reference_distances = []
        
        if corners:
            # Draw detected markers
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            
            # Estimate distance for each marker
            for i, corner in enumerate(corners):
                # Calculate marker width in pixels
                pixel_width = np.linalg.norm(corner[0][0] - corner[0][1])
                
                # Geometric distance calculation
                distance = (self.MARKER_SIZE * 700) / pixel_width
                reference_distances.append(distance)
                
                # Display marker distance
                cv2.putText(frame, f"Ref: {distance:.1f}cm", 
                           tuple(corner[0][0].astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        return np.mean(reference_distances) if reference_distances else None

    def estimate_depth_map(self, frame):
        """Generate depth map using MiDaS model"""
        # Preprocess for depth model
        blob = cv2.dnn.blobFromImage(frame, 1/255.0, (256, 256), (123.675, 116.28, 103.53), True, False)
        self.depth_model.setInput(blob)
        depth_map = self.depth_model.forward()
        
        # Normalize and resize to original dimensions
        depth_map = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
        depth_map = cv2.resize(depth_map[0, 0], (frame.shape[1], frame.shape[0]))
        
        return depth_map

    def calculate_hybrid_distance(self, bbox, depth_map, ref_distance=None):
        """Combine geometric and depth-based distance estimation"""
        x1, y1, x2, y2 = bbox
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        
        # 1. Geometric distance
        pixel_width = x2 - x1
        geometric_dist = (self.MARKER_SIZE * 700) / pixel_width if ref_distance else None
        
        # 2. Depth model distance
        depth_value = depth_map[center_y, center_x]
        depth_dist = depth_value * 0.1  # Scaling factor (calibrate per camera)
        
        # 3. Hybrid approach
        if geometric_dist and ref_distance:
            # Adjust geometric distance based on reference
            adjusted_geo = geometric_dist * (ref_distance / self.MARKER_SIZE)
            hybrid_dist = (adjusted_geo * self.geometric_weight) + \
                          (depth_dist * self.depth_weight)
        else:
            hybrid_dist = depth_dist
        
        return hybrid_dist

    def run(self):
        cap = cv2.VideoCapture(0)
        
        print("🚀 Depth Fusion Detection Started")
        print("Press 'ESC' to quit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Step 1: Detect reference markers
            ref_distance = self.detect_reference_markers(frame)
            
            # Step 2: Generate depth map
            depth_map = self.estimate_depth_map(frame)
            
            # Step 3: Run YOLO detection
            results = self.yolo_model(frame, conf=0.5)
            
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                
                # Step 4: Calculate hybrid distance
                distance = self.calculate_hybrid_distance(
                    (x1, y1, x2, y2), depth_map, ref_distance
                )
                
                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Display distance
                label = f"Dist: {distance:.1f}cm"
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display depth map
            depth_display = cv2.applyColorMap(
                depth_map.astype(np.uint8), cv2.COLORMAP_JET
            )
            cv2.imshow("Depth Map", depth_display)
            cv2.imshow("Depth Fusion Detection", frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = DepthFusionDetector()
    detector.run()
