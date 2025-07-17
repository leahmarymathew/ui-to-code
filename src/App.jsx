import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

// src/App.jsx
// Import your components (will be created in Phase 2)
// import Header from './components/Header';
// import UploadArea from './components/UploadArea';
// import CodeEditor from './components/CodeEditor';
// import ResultDisplay from './components/ResultDisplay';
// import HomePage from './pages/HomePage';
// import AboutPage from './pages/AboutPage';

function App() {
  const [currentPage, setCurrentPage] = useState('home'); // State for navigation
  const [generatedCode, setGeneratedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Placeholder functions for now
  const handleConvert = async (type, input) => {
    setIsLoading(true);
    setErrorMessage('');
    setGeneratedCode('');
    try {
      // This will call your API functions from src/utils/api.js later
      console.log(`Converting ${type} with input:`, input);
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      setGeneratedCode(`<!-- Generated code for ${type} -->\n<div>Hello from ${type} conversion!</div>`);
    } catch (error) {
      console.error('Conversion error:', error);
      setErrorMessage('Failed to convert. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
            {/* Placeholder for Header */}
            <header className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 mb-8">
              <h1 className="text-4xl font-extrabold text-gray-800 text-center">
                UI to Code Converter
              </h1>
              <nav className="mt-4 text-center">
                <button
                  onClick={() => setCurrentPage('home')}
                  className="mx-2 px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => setCurrentPage('about')}
                  className="mx-2 px-4 py-2 rounded-md bg-gray-200 text-gray-800 hover:bg-gray-300 transition-colors"
                >
                  About
                </button>
              </nav>
            </header>

            {/* Placeholder for UploadArea */}
            <section className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 mb-8">
              <h2 className="text-2xl font-semibold text-gray-700 mb-4">Input Your Design</h2>
              <div className="space-y-4">
                <div>
                  <label htmlFor="textInput" className="block text-gray-700 text-sm font-bold mb-2">
                    Text Description:
                  </label>
                  <textarea
                    id="textInput"
                    rows="4"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Describe your UI (e.g., 'A button with blue background and white text')"
                  ></textarea>
                  <button
                    onClick={() => handleConvert('text', 'Sample Text')}
                    className="mt-2 px-4 py-2 rounded-md bg-green-600 text-white hover:bg-green-700 transition-colors"
                  >
                    Convert Text
                  </button>
                </div>
                <div>
                  <label htmlFor="screenshotInput" className="block text-gray-700 text-sm font-bold mb-2">
                    Screenshot Upload:
                  </label>
                  <input
                    type="file"
                    id="screenshotInput"
                    accept="image/*"
                    className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
                  />
                  <button
                    onClick={() => handleConvert('screenshot', 'Sample Screenshot')}
                    className="mt-2 px-4 py-2 rounded-md bg-green-600 text-white hover:bg-green-700 transition-colors"
                  >
                    Convert Screenshot
                  </button>
                </div>
                <div>
                  <label htmlFor="figmaUrlInput" className="block text-gray-700 text-sm font-bold mb-2">
                    Figma URL:
                  </label>
                  <input
                    type="text"
                    id="figmaUrlInput"
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    placeholder="Enter your Figma design URL"
                  />
                  <button
                    onClick={() => handleConvert('figma', 'Sample Figma URL')}
                    className="mt-2 px-4 py-2 rounded-md bg-green-600 text-white hover:bg-green-700 transition-colors"
                  >
                    Convert Figma
                  </button>
                </div>
              </div>
            </section>

            {/* Placeholder for Loading/Error */}
            {isLoading && (
              <div className="w-full max-w-4xl bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded-md mb-4 text-center">
                Loading... Please wait.
              </div>
            )}
            {errorMessage && (
              <div className="w-full max-w-4xl bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md mb-4 text-center">
                {errorMessage}
              </div>
            )}

            {/* Placeholder for CodeEditor and ResultDisplay */}
            {generatedCode && (
              <section className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
                <h2 className="text-2xl font-semibold text-gray-700 mb-4">Generated Code</h2>
                <pre className="bg-gray-800 text-white p-4 rounded-md overflow-auto text-sm">
                  <code>{generatedCode}</code>
                </pre>
                <button
                  onClick={() => navigator.clipboard.writeText(generatedCode)} // Note: Use document.execCommand('copy') for iframe compatibility
                  className="mt-4 px-4 py-2 rounded-md bg-purple-600 text-white hover:bg-purple-700 transition-colors"
                >
                  Copy Code
                </button>
              </section>
            )}
          </div>
        );
      case 'about':
        return (
          <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gray-100">
            <header className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 mb-8">
              <h1 className="text-4xl font-extrabold text-gray-800 text-center">
                About This App
              </h1>
              <nav className="mt-4 text-center">
                <button
                  onClick={() => setCurrentPage('home')}
                  className="mx-2 px-4 py-2 rounded-md bg-gray-200 text-gray-800 hover:bg-gray-300 transition-colors"
                >
                  Home
                </button>
                <button
                  onClick={() => setCurrentPage('about')}
                  className="mx-2 px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
                >
                  About
                </button>
              </nav>
            </header>
            <section className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
              <p className="text-gray-700 text-lg">
                This application aims to convert various design inputs (text descriptions, screenshots, Figma URLs) into functional code. It leverages advanced AI and parsing techniques to streamline the UI development process.
              </p>
              <p className="mt-4 text-gray-700 text-lg">
                Please note that this is a complex project, and the AI models for accurate conversion are under continuous development.
              </p>
            </section>
          </div>
        );
      default:
        return null;
    }
  };

  return renderPage();
}

export default App;
