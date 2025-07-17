// src/components/CodeEditor.jsx
import React from 'react';

function CodeEditor({ code }) {
  const copyToClipboard = () => {
    // Using document.execCommand('copy') for better iframe compatibility
    const el = document.createElement('textarea');
    el.value = code;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    alert('Code copied to clipboard!'); // Replace with a custom modal/toast notification
  };

  return (
    <div className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Generated Code</h2>
      <pre className="bg-gray-800 text-white p-4 rounded-md overflow-auto text-sm max-h-96">
        <code>{code}</code>
      </pre>
      <button
        onClick={copyToClipboard}
        className="mt-4 px-6 py-2 rounded-md bg-purple-600 text-white font-semibold hover:bg-purple-700 transition-colors shadow-md"
      >
        Copy Code
      </button>
    </div>
  );
}

export default CodeEditor;
