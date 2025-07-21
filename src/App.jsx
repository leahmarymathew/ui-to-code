// src/App.jsx
import React, { useState } from 'react';
import Header from './components/Header.jsx';
import HomePage from './pages/HomePage.jsx';
import AboutPage from './pages/AboutPage.jsx';

function App() {
  const [currentPage, setCurrentPage] = useState('home'); // State for navigation

  // Function to render the correct page based on current navigation state
  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        // HomePage will handle its own conversion logic and state
        return <HomePage />;
      case 'about':
        return <AboutPage />;
      default:
        return <HomePage />; // Default to home page
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      {/* Header component for navigation */}
      <Header setCurrentPage={setCurrentPage} currentPage={currentPage} />
      {/* Render the selected page */}
      {renderPage()}
    </div>
  );
}

export default App;