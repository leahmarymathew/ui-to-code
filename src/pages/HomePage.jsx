// src/pages/HomePage.jsx
import React, { useState } from 'react';
import UploadArea from '../components/UploadArea.jsx';
import ResultDisplay from '../components/ResultDisplay.jsx';
import { convertTextToCode, convertScreenshotToCode, convertFigmaToCode } from '../utils/api.js';

function HomePage() {
  const [generatedCode, setGeneratedCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleConvert = async (type, input) => {
    setIsLoading(true);
    setErrorMessage('');
    setGeneratedCode('');
    try {
      let result;
      if (type === 'text') {
        result = await convertTextToCode(input);
      } else if (type === 'screenshot') {
        result = await convertScreenshotToCode(input); // input is FormData here
      } else if (type === 'figma') {
        result = await convertFigmaToCode(input);
      } else {
        throw new Error('Unknown conversion type');
      }

      if (result.code) {
        setGeneratedCode(result.code);
      } else if (result.error) {
        setErrorMessage(result.error);
      } else {
        setErrorMessage('Unexpected response from server.');
      }
    } catch (error) {
      console.error('Conversion error:', error);
      setErrorMessage(`Failed to convert: ${error.message || 'Network error'}. Please try again.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full max-w-4xl">
      <UploadArea onConvert={handleConvert} isLoading={isLoading} />
      <ResultDisplay generatedCode={generatedCode} isLoading={isLoading} errorMessage={errorMessage} />
    </div>
  );
}

export default HomePage;