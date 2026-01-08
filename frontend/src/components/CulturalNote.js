import React, { useState, useEffect } from 'react';
import { Sparkles, X } from 'lucide-react';
import { zelijeCulturalNotes } from '../zelijeData';

const CulturalNote = ({ show, onClose }) => {
  const [currentNote, setCurrentNote] = useState(null);

  useEffect(() => {
    if (show) {
      const randomNote = zelijeCulturalNotes[Math.floor(Math.random() * zelijeCulturalNotes.length)];
      setCurrentNote(randomNote);
    }
  }, [show]);

  if (!show || !currentNote) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6 relative transform transition-all">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
        
        <div className="text-center mb-4">
          <div className="text-6xl mb-3">{currentNote.icon}</div>
          <Sparkles className="w-8 h-8 text-purple-600 mx-auto mb-2" />
          <h3 className="text-2xl font-bold text-gray-800 mb-2">
            Did You Know?
          </h3>
        </div>

        <div className="space-y-4">
          <h4 className="text-xl font-semibold text-purple-700">
            {currentNote.title}
          </h4>
          <p className="text-gray-600 leading-relaxed">
            {currentNote.description}
          </p>
        </div>

        <div className="mt-6 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-500 text-center italic">
            Moroccan Zellige - A Living Tradition
          </p>
        </div>

        <button
          onClick={onClose}
          className="mt-4 w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all"
        >
          Continue Exploring
        </button>
      </div>
    </div>
  );
};

export default CulturalNote;
