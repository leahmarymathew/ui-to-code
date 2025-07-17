// src/pages/AboutPage.jsx
import React from 'react';

function AboutPage() {
  return (
    <section className="w-full max-w-4xl bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">About This App</h2>
      <p className="text-gray-700 text-lg leading-relaxed">
        This application is designed to revolutionize the UI development workflow by converting various design inputs into functional code. Whether you have a simple text description, a visual screenshot, or a detailed Figma design, our goal is to generate clean, semantic, and efficient code for you.
      </p>
      <p className="mt-4 text-gray-700 text-lg leading-relaxed">
        It leverages advanced Artificial Intelligence and sophisticated parsing techniques to understand your design intent and translate it into a coded representation. This project is a complex undertaking, and the underlying AI models for accurate and robust conversion are under continuous development and improvement.
      </p>
      <p className="mt-4 text-gray-700 text-lg leading-relaxed">
        We aim to support various output formats (e.g., HTML/CSS, React components) and constantly enhance the quality and versatility of the generated code. Your feedback is invaluable as we strive to make this tool an indispensable asset for designers and developers alike.
      </p>
    </section>
  );
}

export default AboutPage;