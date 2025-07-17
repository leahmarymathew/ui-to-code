// src/components/UploadArea.jsx
import React, { useState } from 'react';

function UploadArea({ onConvert, isLoading }) {
  const [textInput, setTextInput] = useState('');
  const [screenshotFile, setScreenshotFile] = useState(null);
  const [figmaUrl, setFigmaUrl] = useState('');

  const handleTextConvert = () => {
    if (textInput.trim()) {
      onConvert('text', textInput);
    } else {
      alert('Please enter some text for text-to-code conversion.'); // Using alert for demo, replace with modal
    }
  };

  const handleScreenshotConvert = () => {
    if (screenshotFile) {
      const formData = new FormData();
      formData.append('image', screenshotFile);
      onConvert('screenshot', formData);
    } else {
      alert('Please select a screenshot file.'); // Using alert for demo, replace with modal
    }
  };

  const handleFigmaConvert = () => {
    if (figmaUrl.trim()) {
      onConvert('figma', figmaUrl);
    } else {
      alert('Please enter a Figma URL.'); // Using alert for demo, replace with modal
    }
  };

  return (
    <section className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 mb-8">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Input Your Design</h2>
      <div className="space-y-6"> {/* Increased spacing */}
        {/* Text Input */}
        <div className="p-4 border border-gray-200 rounded-md bg-gray-50">
          <label htmlFor="textInput" className="block text-gray-700 text-sm font-bold mb-2">
            Text Description:
          </label>
          <textarea
            id="textInput"
            rows="4"
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="Describe your UI (e.g., 'A button with blue background and white text')"
            disabled={isLoading}
          ></textarea>
          <button
            onClick={handleTextConvert}
            className="mt-3 px-6 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700 transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? 'Converting...' : 'Convert Text'}
          </button>
        </div>

        {/* Screenshot Upload */}
        <div className="p-4 border border-gray-200 rounded-md bg-gray-50">
          <label htmlFor="screenshotInput" className="block text-gray-700 text-sm font-bold mb-2">
            Screenshot Upload:
          </label>
          <input
            type="file"
            id="screenshotInput"
            accept="image/*"
            onChange={(e) => setScreenshotFile(e.target.files[0])}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          />
          {screenshotFile && (
            <p className="text-sm text-gray-600 mt-2">Selected file: {screenshotFile.name}</p>
          )}
          <button
            onClick={handleScreenshotConvert}
            className="mt-3 px-6 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700 transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? 'Converting...' : 'Convert Screenshot'}
          </button>
        </div>

        {/* Figma URL Input */}
        <div className="p-4 border border-gray-200 rounded-md bg-gray-50">
          <label htmlFor="figmaUrlInput" className="block text-gray-700 text-sm font-bold mb-2">
            Figma URL:
          </label>
          <input
            type="text"
            id="figmaUrlInput"
            value={figmaUrl}
            onChange={(e) => setFigmaUrl(e.target.value)}
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder="Enter your Figma design URL (e.g., https://www.figma.com/file/FILE_ID/...)"
            disabled={isLoading}
          />
          <button
            onClick={handleFigmaConvert}
            className="mt-3 px-6 py-2 rounded-md bg-green-600 text-white font-semibold hover:bg-green-700 transition-colors shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? 'Converting...' : 'Convert Figma'}
          </button>
        </div>
      </div>
    </section>
  );
}

export default UploadArea;