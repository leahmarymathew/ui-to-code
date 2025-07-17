// src/components/Header.jsx
import React from 'react';

function Header({ setCurrentPage, currentPage }) {
  return (
    <header className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6 mb-8">
      <h1 className="text-4xl font-extrabold text-gray-800 text-center">
        UI to Code Converter
      </h1>
      <nav className="mt-4 text-center">
        <button
          onClick={() => setCurrentPage('home')}
          className={`mx-2 px-4 py-2 rounded-md transition-colors ${
            currentPage === 'home' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          Home
        </button>
        <button
          onClick={() => setCurrentPage('about')}
          className={`mx-2 px-4 py-2 rounded-md transition-colors ${
            currentPage === 'about' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-800 hover:bg-gray-300'
          }`}
        >
          About
        </button>
      </nav>
    </header>
  );
}

export default Header;
