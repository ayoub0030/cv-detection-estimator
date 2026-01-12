# Distance Detection Methods

This project contains multiple approaches for calculating object distance using YOLO detection and computer vision techniques.

## 📁 Available Methods

### 1. **Basic Distance Detection** (`distanceWebcam.py`)
Simple geometric distance calculation using object width.

**Features:**
- Single-dimension measurement (width-based)
- Basic smoothing filter
- Lightweight and fast

**Formula:**
```
Distance = (Known_Width × Focal_Length) / Pixel_Width
```

**Usage:**
```bash
python distanceWebcam.py
```

---

### 2. **Advanced Distance Detection** (`advanced_distance_detection.py`)
Multi-strategy approach with filtering and calibration support.

**Features:**
- ✅ Camera calibration support (lens distortion correction)
- ✅ Kalman filtering for noise reduction
- ✅ Multi-frame averaging (10-frame buffer)
- ✅ Dual-dimension calculation (width + height)
- ✅ Confidence-weighted measurements
- ✅ Bounding box stability analysis
- ✅ Quality scoring system (color-coded)

**Usage:**
```bash
# Run detection
python advanced_distance_detection.py

# Run camera calibration (recommended first)
python advanced_distance_detection.py --calibrate
```

**Calibration Process:**
1. Print a 9×6 chessboard pattern
2. Run calibration mode
3. Capture 15-20 images from different angles
4. Press SPACE to capture, ESC when done
5. Generates `camera_calibration.json`

**Controls:**
- `ESC` - Quit
- `C` - Clear tracking history

---

### 3. **Depth Fusion Detection** (`depth_fusion_detection.py`)
Hybrid approach combining geometric and depth estimation.

**Features:**
- ✅ MiDaS depth estimation integration
- ✅ Aruco marker reference scaling
- ✅ Real-time scale calibration
- ✅ Hybrid distance fusion (70% geometric + 30% depth)
- ✅ Visual depth map display

**Usage:**
```bash
python depth_fusion_detection.py
```

**Requirements:**
- Download MiDaS depth model (see setup below)
- Optional: Print Aruco markers for reference scaling

---

## 🎯 Comparison

| Method | Accuracy | Speed | Calibration Required | Best For |
|--------|----------|-------|---------------------|----------|
| Basic | ⭐⭐ | ⚡⚡⚡ | No | Quick testing |
| Advanced | ⭐⭐⭐⭐ | ⚡⚡ | Optional | Production use |
| Depth Fusion | ⭐⭐⭐⭐⭐ | ⚡ | Optional | Maximum accuracy |

---

## 🔧 Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Download Models
1. **YOLO Model**: Already included (`best.pt`)
2. **MiDaS Depth Model** (for depth fusion):
```bash
# Download from GitHub releases
wget https://github.com/isl-org/MiDaS/releases/download/v3_1/dpt_hybrid-midas-501f0c75.pt
```

### Print Reference Materials
- **Chessboard**: [Download 9×6 pattern](https://raw.githubusercontent.com/opencv/opencv/master/doc/pattern.png)
- **Aruco Markers**: Generate at [aruco-marker-generator](https://chev.me/arucogen/)

---

## 📊 Accuracy Tips

### For All Methods:
1. Ensure good lighting conditions
2. Keep camera steady
3. Measure actual object dimensions accurately
4. Test at multiple distances to verify

### For Advanced Method:
1. **Always calibrate your camera first**
2. Use consistent object orientation
3. Allow 2-3 seconds for filters to stabilize

### For Depth Fusion:
1. Place Aruco markers in scene for reference
2. Use 5cm × 5cm markers (default size)
3. Adjust fusion weights based on your camera

---

## 🎨 Visual Indicators

### Advanced Detection Colors:
- 🟢 **Green**: High quality (>70% confidence)
- 🟡 **Yellow**: Medium quality (50-70%)
- 🔴 **Red**: Low quality (<50%)

### Depth Fusion Colors:
- 🔴 **Red**: Close objects
- 🟡 **Yellow**: Medium distance
- 🔵 **Blue**: Far objects

---

## 🐛 Troubleshooting

**Issue**: Distance measurements are inaccurate
- **Solution**: Run camera calibration or adjust `FOCAL_LENGTH` parameter

**Issue**: Detection is slow
- **Solution**: Use basic method or reduce camera resolution

**Issue**: Depth fusion not working
- **Solution**: Ensure MiDaS model is downloaded and path is correct

**Issue**: Measurements fluctuate too much
- **Solution**: Use advanced method with Kalman filtering

---

## 📝 Configuration

### Adjust Object Dimensions
Edit these values in each script:
```python
KNOWN_WIDTH = 4.0   # cm
KNOWN_HEIGHT = 12.0 # cm
```

### Adjust Focal Length (if not calibrated)
```python
FOCAL_LENGTH = 700  # pixels
```

To find your focal length manually:
1. Measure object at known distance (e.g., 50cm)
2. Calculate: `Focal_Length = (Pixel_Width × Distance) / Known_Width`

---

## 🚀 Future Improvements

- [ ] Stereo camera support
- [ ] Multi-object tracking with IDs
- [ ] Distance logging and analytics
- [ ] Mobile app integration
- [ ] Real-time calibration adjustment

---

## 📄 License

Part of the CV Detection Estimator project.
