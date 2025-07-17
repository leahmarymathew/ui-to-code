// src/utils/api.js
// Get the API base URL from environment variables, defaulting for local development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

/**
 * Converts natural language text into code.
 * @param {string} text - The text description of the UI.
 * @returns {Promise<object>} - A promise that resolves to the API response.
 */
export const convertTextToCode = async (text) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/text-to-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (!response.ok) {
            // If response is not OK (e.g., 400, 500), throw an error with details
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error("Error converting text to code:", error);
        throw error; // Re-throw to be caught by the component
    }
};

/**
 * Converts a screenshot image into code.
 * @param {FormData} formData - FormData object containing the image file.
 * @returns {Promise<object>} - A promise that resolves to the API response.
 */
export const convertScreenshotToCode = async (formData) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/screenshot-to-code`, {
            method: 'POST',
            // When sending FormData, the 'Content-Type' header is automatically set
            // to 'multipart/form-data' by the browser, so don't set it manually.
            body: formData
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error("Error converting screenshot to code:", error);
        throw error;
    }
};

/**
 * Converts a Figma design URL into code.
 * @param {string} figmaUrl - The URL of the Figma design file.
 * @returns {Promise<object>} - A promise that resolves to the API response.
 */
export const convertFigmaToCode = async (figmaUrl) => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/figma-to-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: figmaUrl })
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        return response.json();
    } catch (error) {
        console.error("Error converting Figma to code:", error);
        throw error;
    }
};
