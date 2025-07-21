
# UI to Code Converter Application

## Project Overview

The UI to Code Converter is an innovative application designed to streamline the front-end development process by transforming various design inputs into functional code. Leveraging advanced AI models and sophisticated parsing techniques, this tool aims to convert natural language descriptions, visual screenshots, and Figma design URLs directly into clean HTML and Tailwind CSS.

This project demonstrates a full-stack approach using React for the frontend, Flask for the backend API, and integrates a powerful Large Language Model (LLM) hosted on Google Colab for AI inference, bypassing local hardware limitations.

## Features

* **Text to Code:** Convert natural language UI descriptions (e.g., "a blue button with white text", "a responsive navigation bar") into HTML/Tailwind CSS.
* **Screenshot to Code (Placeholder):** Future capability to convert UI screenshots into code using Computer Vision. Currently uses a placeholder.
* **Figma to Code (Placeholder):** Future capability to convert Figma design URLs into code by parsing Figma API data. Currently uses a placeholder.
* **Responsive UI:** A user-friendly interface built with React and Tailwind CSS.
* **Modular Backend:** Flask API serving as a bridge between the frontend and AI services.
* **Cloud AI Integration:** Utilizes Google Colab's free GPU resources to run a powerful LLM (Mistral-7B) for faster AI inference.

## Technologies Used

**Frontend:**
* **React:** A JavaScript library for building user interfaces.
* **Vite:** A fast build tool for modern web projects.
* **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

**Backend (Local Flask API):**
* **Python:** The programming language.
* **Flask:** A lightweight web framework for building APIs.
* **Flask-CORS:** Enables Cross-Origin Resource Sharing.
* **python-dotenv:** For managing environment variables.
* **requests:** For making HTTP requests to the Colab AI endpoint.

**AI Inference Endpoint (Google Colab):**
* **Python:** For scripting.
* **Google Colab:** Free cloud platform for running Python notebooks with GPU access.
* **`mistralai/Mistral-7B-Instruct-v0.2`:** The Large Language Model used for text-to-code generation (hosted on Colab).
* **Hugging Face Transformers:** Library for working with LLMs.
* **PyTorch:** Deep learning framework used by the LLM.
* **Accelerate & BitsAndBytes:** For efficient (4-bit quantized) loading of LLMs onto GPU.
* **`pyngrok`:** A Python wrapper for `ngrok`, used to create a public URL for the Colab-hosted Flask app.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Node.js** (LTS version recommended) & **npm** (comes with Node.js)
* **Python 3.8+**
* **pip** (comes with Python)
* A **Hugging Face Account** (and a Read access token)
* A **Google Account** (for Google Colab access)
* An **ngrok Account** (free tier is sufficient for the auth token)

## Setup and Installation Guide

Follow these steps carefully to get the application running locally and connect to the Colab-hosted AI.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-app-name.git](https://github.com/your-username/your-app-name.git) # Replace with your repo URL
cd your-app-name
````

### 2\. Backend Setup (Local Flask API)

1.  **Create a Python Virtual Environment:**
    ```bash
    cd server
    python -m venv venv
    ```
2.  **Activate the Virtual Environment:**
      * Windows: `.\venv\Scripts\activate`
      * macOS/Linux: `source venv/bin/activate`
3.  **Install Backend Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Your `requirements.txt` should contain `Flask`, `Flask-CORS`, `python-dotenv`, `requests`). If `requirements.txt` is missing, you can create it by running `pip freeze > requirements.txt` after manually installing those packages.)
4.  **Return to Project Root:**
    ```bash
    cd ..
    ```

### 3\. Frontend Setup (Local React App)

1.  **Install Frontend Dependencies:**
    ```bash
    npm install
    ```

### 4\. Environment Variables (`.env` file)

Create a `.env` file in the **root directory** of your project (`your-app-name/.env`).

```dotenv
# .env

# Frontend API Base URL (for React's fetch calls)
# Ensure this matches your local Flask backend port
VITE_API_BASE_URL=http://localhost:5000

# Backend Flask configuration
FLASK_APP=server/app.py
FLASK_RUN_PORT=5000

# Figma API Key (Replace with your actual key from Figma developer settings)
# Get it from: [https://www.figma.com/developers/api](https://www.figma.com/developers/api)
FPGMA_API_KEY=your_figma_personal_access_token_here

# Colab AI Inference Endpoint URL (THIS WILL BE UPDATED LATER)
COLAB_AI_API_URL=
```

**Important:** Do NOT commit your `.env` file to Git. It's listed in `.gitignore`.

### 5\. AI Model Setup (Google Colab Integration)

This is where you set up the GPU-powered AI endpoint.

1.  **Open the Colab Notebook:**
    Go to [Google Colab](https://colab.research.google.com/) and create a new notebook.
    You will transfer the Colab-specific code into cells in this notebook.

2.  **Configure Colab Runtime:**

      * In the Colab notebook, go to `Runtime > Change runtime type`.
      * Select `GPU` for `Hardware accelerator` (preferably A100/L4 if available, otherwise T4). Click `Save`.

3.  **Install Libraries in Colab (First Cell):**
    Copy this code into the **first cell** of your Colab notebook and run it.

    ```python
    # Install core libraries (excluding torch, torchvision, torchaudio for now, as we'll install them specifically)
    !pip install -q Flask Flask-Cors transformers -U bitsandbytes accelerate sentencepiece protobuf pyngrok

    # --- IMPORTANT: Install PyTorch with compatible torchvision/torchaudio for CUDA ---
    # First, run !nvidia-smi in a new Colab cell to find your CUDA Version (e.g., CUDA Version: 12.4).
    # Then, use the matching index-url. Example for CUDA 12.4:
    !pip install -q torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu124](https://download.pytorch.org/whl/cu124)

    # Login to Hugging Face (optional but recommended for rate limits and gated models)
    # You'll be prompted to enter your Hugging Face token interactively.
    # Get your token from: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (ensure 'Read' access)
    from huggingface_hub import login
    try:
        login()
    except Exception as e:
        print(f"Hugging Face login failed (this might be okay if the model is public): {e}")

    print("Libraries installed and Hugging Face login attempted.")
    ```

4.  **Download and Load the AI Model in Colab (Second Cell):**
    Copy this code into the **second cell** of your Colab notebook and run it.

    ```python
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

    # Define the model name (Mistral-7B-Instruct-v0.2 is chosen for its capability)
    MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

    print(f"--- Starting Model Download and Loading for {MODEL_NAME} ---")

    try:
        # Load tokenizer
        print("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        # Load model with quantization for efficient GPU usage (4-bit quantization)
        print("Loading model...")
        # `load_in_4bit=True` requires `bitsandbytes` and `accelerate`.
        # `device_map="auto"` ensures optimal use of GPU memory.
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16, 
            device_map="auto",         
            load_in_4bit=True          
        )
        print("Model loaded successfully.")

        # Create a text generation pipeline
        print("Creating text generation pipeline...")
        # Ensure pad_token_id is set for proper generation stopping.
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id 
        
        nlp_pipeline_colab = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            # IMPORTANT: Do NOT pass 'device' argument here, as 'device_map="auto"' with accelerate handles it.
        )
        print("NLP Pipeline initialized.")

    except Exception as e:
        print(f"ERROR: Could not load model or pipeline: {e}")
        nlp_pipeline_colab = None # Set to None if loading fails

    print("--- Model Setup Complete ---")
    ```

    **Note:** `mistralai/Mistral-7B-Instruct-v0.2` is a "gated" model. You MUST go to its Hugging Face page (`https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2`), log in to Hugging Face, and **click "Request access"** (or similar) to accept its terms before downloading.

5.  **Create Flask API Endpoint in Colab (Third Cell):**
    Copy this code into the **third cell** of your Colab notebook and run it.

    ````python
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    from pyngrok import ngrok # For tunneling

    # --- Flask App Setup ---
    colab_app = Flask(__name__)
    CORS(colab_app) # Enable CORS for this Colab Flask app

    # --- API Endpoint for Code Generation ---
    @colab_app.route('/generate-code', methods=['POST'])
    def generate_code():
        if not nlp_pipeline_colab: # Check if the model loaded successfully in the previous cell
            return jsonify({"error": "AI model not loaded on Colab. Check previous cell output."}), 500

        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in request body."}), 400

        text_description = data['text']
        print(f"[Colab AI] Received request: '{text_description}'")

        try:
            # Mistral Instruct prompt format (CRITICAL for Mistral models)
            # This guides the model to act as a code generator.
            messages = [
                {"role": "user", "content": f"Generate clean HTML and Tailwind CSS code for the following UI description: {text_description}"},
            ]
            prompt = nlp_pipeline_colab.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            # Generate code using the loaded model
            generation_output = nlp_pipeline_colab(
                prompt,
                max_new_tokens=1024, # Adjust based on expected code length
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                pad_token_id=nlp_pipeline_colab.tokenizer.eos_token_id # Ensure proper stopping
            )

            generated_text = generation_output[0]['generated_text']

            # Post-process: Extract only the generated code part.
            # Mistral often includes the full prompt and sometimes markdown fences.
            code = generated_text.split("[/INST]")[-1].strip() # Remove the prompt template part
            
            # Further clean markdown fences (e.g., ```html...```)
            if code.startswith('```html'):
                code = code[7:].strip()
                if code.endswith('```'):
                    code = code[:-3].strip()
            elif code.startswith('```'): # Generic markdown block
                code_lines = code.split('\n')
                if len(code_lines) > 2:
                    code = '\n'.join(code_lines[1:-1]).strip()

            print(f"[Colab AI] Generated code (first 200 chars):\n{code[:200]}...")
            return jsonify({"code": code}), 200

        except Exception as e:
            print(f"[Colab AI] Error during code generation: {e}")
            return jsonify({"error": "Failed to generate code.", "details": str(e)}), 500

    # --- ngrok Tunnel Setup ---
    # Get your ngrok auth token from https://dashboard.ngrok.com/get-started/your-authtoken
    # You'll need to create a free account.
    # Run !ngrok authtoken YOUR_NGROK_AUTHTOKEN in a new Colab cell ONCE.
    # Example: !ngrok authtoken 2P4P05B17H221R33X33B6H6K7V7M0A4M8G6S8V6B9

    # Start ngrok tunnel
    PORT = 5001 # Choose a port for the Colab Flask app
    public_url = ngrok.connect(PORT)
    print(f"🚀 Colab Flask app running on: http://localhost:{PORT}")
    print(f"🌍 Public ngrok URL: {public_url}")

    # Run the Flask app
    colab_app.run(port=PORT, debug=False)
    ````

    **Before running this cell:** In a **new, separate Colab cell**, run `!ngrok authtoken YOUR_NGROK_AUTHTOKEN` (replace with your actual token). Run that cell once, then proceed with the main Flask API cell.

6.  **Get the Public `ngrok` URL:** After running the Flask API cell in Colab, copy the `https://YOUR_RANDOM_ID.ngrok-free.app` URL.

7.  **Update Your Local `.env` File (Final Step for `COLAB_AI_API_URL`):**
    In your project's root directory (`your-app-name/.env`), set:

    ```dotenv
    COLAB_AI_API_URL=YOUR_COPIED_NGROK_URL_HERE/generate-code
    ```

    (Remember to include `/generate-code` at the end\!)

### 6\. Run the Application

1.  **Ensure Colab is Running:** Keep your Google Colab tab **open and connected** to the runtime. If it disconnects, you'll need to rerun the relevant Colab cells to get a new `ngrok` URL and update your local `.env`.
2.  **Start Local Flask Backend:**
    Open your terminal, navigate to `your-app-name/server`, activate your virtual environment, and run:
    ```bash
    python app.py
    ```
3.  **Start Local React Frontend:**
    Open a **new** terminal, navigate to your project root `your-app-name/`, and run:
    ```bash
    npm run dev
    ```
4.  **Open in Browser:** Access your frontend application at `http://localhost:5173/` (or whatever Vite displays).

## Usage

1.  Navigate to the "Home" page.
2.  In the "Text Description" field, enter a description of the UI component you want to generate (e.g., "A button with a blue background and white text", "A simple login form with username and password inputs and a submit button").
3.  Click "Convert Text".
4.  Wait for the generated code to appear in the "Generated Code" section. (Initial requests might take a bit longer as the Colab instance warms up).
5.  You can then copy the generated code to your clipboard.

## Project Structure

```
your-app-name/
├── .env                 # Environment variables (IGNORED by Git)
├── .gitignore           # Git ignore rules
├── package.json         # Frontend dependencies
├── public/              # Frontend static assets
│   └── index.html
│   └── vite.svg
├── src/                 # Frontend source code (React)
│   ├── components/      # Reusable React components (Header, UploadArea, CodeEditor, ResultDisplay)
│   ├── pages/           # Main application pages (HomePage, AboutPage)
│   ├── styles/          # Global CSS (index.css)
│   ├── utils/           # Utility functions (api.js for backend calls)
│   ├── App.jsx          # Main React application component
│   └── main.jsx         # Vite's React entry point
├── server/              # Backend source code (Flask)
│   ├── venv/            # Python virtual environment (IGNORED by Git)
│   ├── app.py           # Flask application entry point
│   ├── requirements.txt # Python dependencies list
│   ├── routes/          # API endpoint definitions
│   │   ├── __init__.py
│   │   ├── figma_to_code.py
│   │   ├── screenshot_to_code.py
│   │   └── text_to_code.py
│   ├── services/        # Business logic / AI integration (e.g., nlp_service.py calls Colab)
│   │   ├── __init__.py
│   │   ├── figma_service.py
│   │   ├── nlp_service.py
│   │   └── vision_service.py
│   ├── models/          # Directory for AI model files (locally downloaded - IGNORED by Git)
│   │   └── __init__.py
│   └── uploads/         # Temporary file uploads (IGNORED by Git)
└── vite.config.js       # Vite configuration file
```

## Future Enhancements

  * **Implement Screenshot to Code:** Integrate a Computer Vision model (e.g., YOLO, Mask R-CNN) for UI element detection and layout analysis.
  * **Implement Figma to Code:** Develop robust parsing logic for Figma's API data to translate design properties into precise code.
  * **Support More Code Formats:** Extend generation to React components, Vue components, etc.
  * **Live Preview:** Add a sandbox or iframe to render the generated code live.
  * **Code Refinement:** Implement code quality checks, best practices, and optimization for generated code.
  * **User Authentication:** For more advanced features or private designs.
  * **Deployment:** Deploy the frontend (e.g., Vercel, Netlify) and backend (e.g., Render, Google Cloud Run) to cloud platforms.

