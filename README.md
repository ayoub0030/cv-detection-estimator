# Moroccan Zellige Detector Web App

A modern web application for detecting Moroccan Zellige patterns using YOLOv8 deep learning model.

## Features

- 🖼️ **Image Upload Detection**: Upload images and detect Zellige patterns
- 📹 **Real-time Webcam Detection**: Capture and analyze images from your webcam
- 🎨 **Beautiful UI**: Modern, responsive interface with TailwindCSS
- ⚡ **Fast Inference**: Powered by YOLOv8 for accurate real-time detection
- 📊 **Detailed Results**: View confidence scores and detection counts

## Tech Stack

### Backend
- Flask (Python web framework)
- YOLOv8 (Ultralytics)
- OpenCV (Image processing)
- Flask-CORS (Cross-origin support)

### Frontend
- React 18
- TailwindCSS (Styling)
- Axios (API calls)
- Lucide React (Icons)
- React Webcam (Camera access)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r backend-requirements.txt
```

2. Ensure `best.pt` model file is in the root directory

3. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Install TailwindCSS and PostCSS:
```bash
npm install -D tailwindcss postcss autoprefixer
```

4. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

### Image Upload Mode
1. Click on "Upload Image" tab
2. Select an image containing Moroccan Zellige patterns
3. Click "Detect Zellige" button
4. View detection results with bounding boxes and confidence scores

### Webcam Mode
1. Click on "Webcam" tab
2. Allow camera access when prompted
3. Position the camera to capture Zellige patterns
4. Click "Capture & Detect" button
5. View real-time detection results

## API Endpoints

### `POST /api/detect`
Upload an image for detection
- **Body**: FormData with `image` file
- **Response**: JSON with detections and annotated image

### `POST /api/detect-webcam`
Detect from webcam capture
- **Body**: JSON with base64 encoded image
- **Response**: JSON with detections and annotated image

### `GET /api/health`
Check API health status
- **Response**: JSON with status and model info

## Building for Production

### Frontend Build
```bash
cd frontend
npm run build
```

The Flask app will automatically serve the built React app from the `/` route.

### Running Production Server
```bash
python app.py
```

Access the app at `http://localhost:5000`

## Model Information

- **Model**: YOLOv8 trained on Moroccan Zellige dataset
- **File**: `best.pt`
- **Confidence Threshold**: 0.25
- **Detection Class**: Moroccan Zellige patterns

## Project Structure

```
yolo-helmet/
├── app.py                      # Flask backend server
├── best.pt                     # YOLOv8 trained model
├── backend-requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
├── uploads/                    # Uploaded images (auto-created)
└── results/                    # Detection results (auto-created)
```

## License

MIT

## Credits

Built with ❤️ using YOLOv8, React, and Flask
