import React, { useState, useRef, useCallback } from 'react';
import axios from 'axios';
import Webcam from 'react-webcam';
import { Upload, Camera, Image as ImageIcon, Sparkles, AlertCircle, CheckCircle, BookOpen } from 'lucide-react';
import CulturalNote from './components/CulturalNote';
import ExploreTab from './components/ExploreTab';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [activeTab, setActiveTab] = useState('upload');
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [webcamActive, setWebcamActive] = useState(false);
  const [showCulturalNote, setShowCulturalNote] = useState(false);
  const webcamRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultImage(null);
      setDetections([]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post(`${API_URL}/detect`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setResultImage(response.data.image);
      setDetections(response.data.detections);
      if (response.data.detections.length > 0) {
        setShowCulturalNote(true);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Detection failed');
    } finally {
      setLoading(false);
    }
  };

  const captureWebcam = useCallback(async () => {
    if (!webcamRef.current) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/detect-webcam`, {
        image: imageSrc
      });

      setResultImage(response.data.image);
      setDetections(response.data.detections);
      if (response.data.detections.length > 0) {
        setShowCulturalNote(true);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Detection failed');
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="w-10 h-10 text-yellow-300" />
            <h1 className="text-5xl font-bold text-white">Moroccan Zellige Detector</h1>
            <Sparkles className="w-10 h-10 text-yellow-300" />
          </div>
          <p className="text-purple-100 text-lg">AI-powered detection of traditional Moroccan Zellige patterns</p>
        </div>

        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex-1 py-4 px-6 font-semibold transition-all flex items-center justify-center gap-2 ${
                activeTab === 'upload'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Upload className="w-5 h-5" />
              Upload Image
            </button>
            <button
              onClick={() => {
                setActiveTab('webcam');
                setWebcamActive(true);
              }}
              className={`flex-1 py-4 px-6 font-semibold transition-all flex items-center justify-center gap-2 ${
                activeTab === 'webcam'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Camera className="w-5 h-5" />
              Webcam
            </button>
            <button
              onClick={() => setActiveTab('explore')}
              className={`flex-1 py-4 px-6 font-semibold transition-all flex items-center justify-center gap-2 ${
                activeTab === 'explore'
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              <BookOpen className="w-5 h-5" />
              Explore
            </button>
          </div>

          <div className="p-8">
            {activeTab === 'upload' && (
              <div className="space-y-6">
                <div className="border-2 border-dashed border-purple-300 rounded-xl p-12 text-center hover:border-purple-500 transition-colors">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer">
                    <ImageIcon className="w-16 h-16 mx-auto text-purple-400 mb-4" />
                    <p className="text-gray-600 text-lg mb-2">
                      Click to upload or drag and drop
                    </p>
                    <p className="text-gray-400 text-sm">PNG, JPG, JPEG up to 10MB</p>
                  </label>
                </div>

                {previewUrl && (
                  <div className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <h3 className="text-lg font-semibold mb-3 text-gray-700">Original Image</h3>
                        <img
                          src={previewUrl}
                          alt="Preview"
                          className="w-full rounded-lg shadow-md"
                        />
                      </div>
                      {resultImage && (
                        <div>
                          <h3 className="text-lg font-semibold mb-3 text-gray-700">Detection Result</h3>
                          <img
                            src={resultImage}
                            alt="Result"
                            className="w-full rounded-lg shadow-md"
                          />
                        </div>
                      )}
                    </div>

                    <button
                      onClick={handleUpload}
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-lg font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                    >
                      {loading ? 'Detecting...' : 'Detect Zellige'}
                    </button>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'webcam' && (
              <div className="space-y-6">
                <div className="relative rounded-xl overflow-hidden bg-black">
                  {webcamActive ? (
                    <Webcam
                      ref={webcamRef}
                      screenshotFormat="image/jpeg"
                      className="w-full"
                      videoConstraints={{
                        width: 1280,
                        height: 720,
                        facingMode: 'user'
                      }}
                    />
                  ) : (
                    <div className="aspect-video flex items-center justify-center">
                      <Camera className="w-24 h-24 text-gray-400" />
                    </div>
                  )}
                </div>

                {resultImage && (
                  <div>
                    <h3 className="text-lg font-semibold mb-3 text-gray-700">Detection Result</h3>
                    <img
                      src={resultImage}
                      alt="Webcam Result"
                      className="w-full rounded-lg shadow-md"
                    />
                  </div>
                )}

                <button
                  onClick={captureWebcam}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-lg font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
                >
                  {loading ? 'Detecting...' : 'Capture & Detect'}
                </button>
              </div>
            )}

            {activeTab === 'explore' && (
              <ExploreTab />
            )}

            {error && (
              <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-red-700">{error}</p>
              </div>
            )}

            {detections.length > 0 && (
              <div className="mt-6 bg-green-50 border border-green-200 rounded-lg p-6">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                  <h3 className="text-xl font-semibold text-green-800">
                    Detected {detections.length} Zellige Pattern{detections.length !== 1 ? 's' : ''}
                  </h3>
                </div>
                <div className="space-y-2">
                  {detections.map((det, idx) => (
                    <div key={idx} className="bg-white rounded-lg p-4 shadow-sm">
                      <div className="flex justify-between items-center">
                        <span className="font-semibold text-gray-800">{det.class}</span>
                        <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                          {(det.confidence * 100).toFixed(1)}% confidence
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 text-center text-white text-sm">
          <p>Powered by YOLOv8 • Built with React & Flask</p>
        </div>
      </div>

      <CulturalNote 
        show={showCulturalNote} 
        onClose={() => setShowCulturalNote(false)} 
      />
    </div>
  );
}

export default App;
