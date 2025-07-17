// src/components/ResultDisplay.jsx
import React from 'react';
import CodeEditor from './CodeEditor.jsx'; // Import CodeEditor

function ResultDisplay({ generatedCode, isLoading, errorMessage }) {
  return (
    <>
      {isLoading && (
        <div className="w-full max-w-4xl bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded-md mb-4 text-center shadow-md">
          <div className="flex items-center justify-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading... Please wait.
          </div>
        </div>
      )}

      {errorMessage && (
        <div className="w-full max-w-4xl bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md mb-4 text-center shadow-md">
          <p className="font-bold">Error!</p>
          <p>{errorMessage}</p>
        </div>
      )}

      {generatedCode && !isLoading && !errorMessage && (
        <CodeEditor code={generatedCode} />
      )}
    </>
  );
}

export default ResultDisplay;
