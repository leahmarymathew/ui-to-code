

The **UI to Code Converter** is an application designed to accelerate front-end development by transforming design inputs into functional code. It leverages advanced AI models and parsing techniques to convert:

* Natural language descriptions (e.g., “a blue button with white text”, “a responsive navigation bar”)
* Visual screenshots (planned feature)
* Figma design URLs (planned feature)

…into clean HTML and Tailwind CSS.

This project showcases a full-stack implementation using **React** for the frontend, **Flask** for the backend API, and a **Large Language Model (LLM)** hosted on Google Colab for AI inference, eliminating local hardware limitations.

## Features

* **Text to Code:** Converts natural language UI descriptions into HTML/Tailwind CSS.
* **Screenshot to Code (Placeholder):** Planned capability to process UI screenshots with computer vision.
* **Figma to Code (Placeholder):** Planned capability to convert Figma designs using Figma API integration.
* **Responsive UI:** Built with React and Tailwind CSS for a seamless experience.
* **Modular Backend:** Flask API bridges frontend and AI services.
* **Cloud AI Integration:** Utilizes Google Colab’s GPU resources to run a powerful LLM (Mistral-7B) for efficient AI inference.

## Technologies Used

**Frontend**

* React (with Vite)
* Tailwind CSS

**Backend**

* Python (Flask)
* Flask-CORS
* python-dotenv
* requests

**AI Inference Endpoint (Google Colab)**

* Hugging Face Transformers (Mistral-7B-Instruct-v0.2)
* PyTorch
* Accelerate and BitsAndBytes (for efficient GPU loading)
* pyngrok (for public URL exposure)

## Prerequisites

Before running the application, ensure the following are installed:

* Node.js (LTS version recommended) and npm
* Python 3.8+ and pip
* Hugging Face account (with read access token)
* Google account (for Google Colab access)
* ngrok account (free tier is sufficient)

## Setup and Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-app-name.git
cd your-app-name
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd ../backend
pip install -r requirements.txt
```

4. Start the frontend:

```bash
cd frontend
npm run dev
```

5. Start the backend:

```bash
cd ../backend
python app.py
```

6. Connect Google Colab for AI inference and expose the endpoint using ngrok.


