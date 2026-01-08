import React, { useState } from 'react';
import { BookOpen, Palette, Hammer, Lightbulb } from 'lucide-react';
import { zelijeGallery, zelijeFacts, zelijeProcess } from '../zelijeData';

const ExploreTab = () => {
  const [activeSection, setActiveSection] = useState('gallery');
  const [selectedImage, setSelectedImage] = useState(null);

  return (
    <div className="space-y-6">
      <div className="text-center mb-6">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Explore Moroccan Zellige
        </h2>
        <p className="text-gray-600">
          Discover the rich history and artistry of traditional Moroccan tilework
        </p>
      </div>

      <div className="flex gap-2 overflow-x-auto pb-2">
        <button
          onClick={() => setActiveSection('gallery')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
            activeSection === 'gallery'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <Palette className="w-5 h-5" />
          Gallery
        </button>
        <button
          onClick={() => setActiveSection('process')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
            activeSection === 'process'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <Hammer className="w-5 h-5" />
          Crafting Process
        </button>
        <button
          onClick={() => setActiveSection('facts')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
            activeSection === 'facts'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <Lightbulb className="w-5 h-5" />
          Fun Facts
        </button>
        <button
          onClick={() => setActiveSection('about')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition-all ${
            activeSection === 'about'
              ? 'bg-purple-600 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          <BookOpen className="w-5 h-5" />
          About
        </button>
      </div>

      {activeSection === 'gallery' && (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {zelijeGallery.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow cursor-pointer"
              onClick={() => setSelectedImage(item)}
            >
              <img
                src={item.imageUrl}
                alt={item.title}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <div className="text-xs text-purple-600 font-semibold mb-1">
                  {item.category}
                </div>
                <h3 className="font-bold text-gray-800 mb-2">{item.title}</h3>
                <p className="text-sm text-gray-600">{item.description}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeSection === 'process' && (
        <div className="space-y-4">
          {zelijeProcess.map((step) => (
            <div
              key={step.step}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {step.step}
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-gray-800 mb-2">
                    {step.title}
                  </h3>
                  <p className="text-gray-600">{step.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeSection === 'facts' && (
        <div className="grid md:grid-cols-2 gap-4">
          {zelijeFacts.map((item, idx) => (
            <div
              key={idx}
              className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <div className="text-4xl mb-3">{item.emoji}</div>
              <p className="text-gray-700 leading-relaxed">{item.fact}</p>
            </div>
          ))}
        </div>
      )}

      {activeSection === 'about' && (
        <div className="bg-white rounded-lg shadow-md p-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-4">
            The Art of Zellige
          </h3>
          <div className="space-y-4 text-gray-600 leading-relaxed">
            <p>
              Zellige (زليج) is a distinctive element of Moroccan architecture, consisting of
              geometrically patterned mosaics made from individually hand-chiseled tile pieces.
              This ancient art form has been practiced for over a millennium, with techniques
              passed down through generations of master craftsmen.
            </p>
            <p>
              The creation of Zellige is a labor-intensive process that requires years of training
              and exceptional skill. Each tile is cut by hand using traditional tools, and the
              patterns are assembled piece by piece to create intricate geometric designs that
              reflect Islamic artistic principles.
            </p>
            <p>
              Today, Zellige continues to be an important part of Moroccan cultural heritage,
              adorning everything from historic monuments to modern homes. The craft represents
              not just artistic excellence, but also mathematical precision, cultural identity,
              and the enduring legacy of Moroccan craftsmanship.
            </p>
            <div className="mt-6 p-4 bg-purple-50 rounded-lg border-l-4 border-purple-600">
              <p className="text-purple-900 font-semibold">
                "Zellige is not just decoration—it is mathematics, poetry, and spirituality
                expressed through color and form."
              </p>
              <p className="text-purple-700 text-sm mt-2">— Traditional Moroccan Proverb</p>
            </div>
          </div>
        </div>
      )}

      {selectedImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div className="bg-white rounded-2xl max-w-3xl w-full overflow-hidden">
            <img
              src={selectedImage.imageUrl}
              alt={selectedImage.title}
              className="w-full h-96 object-cover"
            />
            <div className="p-6">
              <div className="text-sm text-purple-600 font-semibold mb-2">
                {selectedImage.category}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">
                {selectedImage.title}
              </h3>
              <p className="text-gray-600">{selectedImage.description}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExploreTab;
