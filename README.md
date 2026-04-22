
# UI to Code Converter Application

## Project Overview

The UI to Code Converter is a full-stack web application that transforms design inputs into functional HTML and Tailwind CSS code. It accepts three types of input: a plain-text UI description, a screenshot image, or a Figma design URL, and returns ready-to-use front-end code.

The frontend is built with React 19 and Vite, the backend is a Python Flask API, and text-to-code generation is powered by a Large Language Model (Mistral-7B-Instruct) running on a free Google Colab GPU instance, exposed to the local backend via an ngrok tunnel. This architecture lets you leverage powerful AI inference without any local GPU requirement.

## Features

* **Text to Code:** Convert natural language UI descriptions (e.g., "a blue button with white text", "a responsive navigation bar") into HTML/Tailwind CSS via a Mistral-7B model hosted on Google Colab.
* **Screenshot to Code (Placeholder):** Upload a UI screenshot; full Computer Vision inference is planned for a future release. Currently returns a styled placeholder response.
* **Figma to Code (Placeholder):** Paste a Figma design URL; full Figma API parsing is planned for a future release. Currently fetches Figma data and returns a placeholder response.
* **Responsive UI:** Single-page React app with state-based navigation (Home / About) and Tailwind CSS styling.
* **Modular Backend:** Flask API with Blueprint-based routing (`/api/text-to-code`, `/api/screenshot-to-code`, `/api/figma-to-code`).
* **Cloud AI Integration:** Uses Google Colab's free GPU resources to run Mistral-7B-Instruct-v0.2 with 4-bit quantisation for fast inference, tunnelled via ngrok.
* **Local Fallback:** When `COLAB_AI_API_URL` is not set, the NLP service falls back to a set of keyword-based HTML/Tailwind snippets so the app remains usable offline.

## Technologies Used

**Frontend:**
* **React 19** – component-based UI library.
* **Vite 7** – fast development server and build tool.
* **Tailwind CSS 4** – utility-first CSS framework.

**Backend (Local Flask API):**
* **Python 3.8+**
* **Flask 3** – lightweight web framework.
* **Flask-CORS** – Cross-Origin Resource Sharing support.
* **python-dotenv** – environment variable management.
* **requests** – HTTP client used by the NLP service to call the Colab endpoint.

**AI Inference Endpoint (Google Colab):**
* **Google Colab** – free cloud GPU platform.
* **`mistralai/Mistral-7B-Instruct-v0.2`** – LLM used for text-to-code generation.
* **Hugging Face Transformers** – model loading and text-generation pipeline.
* **PyTorch** – deep learning runtime.
* **Accelerate & BitsAndBytes** – 4-bit quantised model loading.
* **`pyngrok`** – creates a public HTTPS tunnel to the Colab Flask server.

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
git clone https://github.com/leahmarymathew/ui-to-code.git
cd ui-to-code
```

### 2. Backend Setup (Local Flask API)

1.  **Create a Python Virtual Environment** (from the project root):
    ```bash
    python -m venv venv
    ```
2.  **Activate the Virtual Environment:**
      * Windows: `.\venv\Scripts\activate`
      * macOS/Linux: `source venv/bin/activate`
3.  **Install Backend Dependencies** (the `requirements.txt` is in the project root):
    ```bash
    pip install -r requirements.txt
    pip install requests  # add requests if not already listed
    ```

### 3. Frontend Setup (Local React App)

1.  **Install Frontend Dependencies:**
    ```bash
    npm install
    ```

### 4. Environment Variables (`.env` file)

Create a `.env` file in the **project root** (`ui-to-code/.env`).

```dotenv
# .env

# Frontend API Base URL (for React's fetch calls)
# Ensure this matches your local Flask backend port
VITE_API_BASE_URL=http://localhost:5000

# Backend Flask configuration
FLASK_APP=server/app.py
FLASK_RUN_PORT=5000

# Figma API Key (Replace with your actual key from Figma developer settings)
# Get it from: https://www.figma.com/developers/api
# Note: the env var name in code is intentionally FPGMA_API_KEY
FPGMA_API_KEY=your_figma_personal_access_token_here

# Colab AI Inference Endpoint URL (set after running the Colab notebook)
COLAB_AI_API_URL=
```

**Important:** Do NOT commit your `.env` file to Git. It is listed in `.gitignore`.

### 5. AI Model Setup (Google Colab Integration)

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
    !pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

    # Login to Hugging Face (optional but recommended for rate limits and gated models)
    # You'll be prompted to enter your Hugging Face token interactively.
    # Get your token from: https://huggingface.co/settings/tokens (ensure 'Read' access)
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
    In your project's root directory (`ui-to-code/.env`), set:

    ```dotenv
    COLAB_AI_API_URL=YOUR_COPIED_NGROK_URL_HERE/generate-code
    ```

    (Remember to include `/generate-code` at the end!)

### 6. Run the Application

1.  **Ensure Colab is Running:** Keep your Google Colab tab **open and connected** to the runtime. If it disconnects, rerun the relevant Colab cells to get a new `ngrok` URL and update your local `.env`.
2.  **Start Local Flask Backend** (from the project root, with virtual environment activated):
    ```bash
    python server/app.py
    ```
3.  **Start Local React Frontend** (from the project root in a new terminal):
    ```bash
    npm run dev
    ```
4.  **Open in Browser:** Navigate to `http://localhost:5173/` (or the URL shown by Vite).

## Usage

1.  Navigate to the "Home" page.
2.  In the "Text Description" field, enter a description of the UI component you want to generate (e.g., "A button with a blue background and white text", "A simple login form with username and password inputs and a submit button").
3.  Click "Convert Text".
4.  Wait for the generated code to appear in the "Generated Code" section. (Initial requests might take a bit longer as the Colab instance warms up).
5.  You can then copy the generated code to your clipboard.

## Project Structure

```
ui-to-code/
├── .env                   # Environment variables (IGNORED by Git)
├── .gitignore             # Git ignore rules
├── index.html             # Vite HTML entry point
├── package.json           # Frontend dependencies (React, Vite, Tailwind CSS)
├── requirements.txt       # Python backend dependencies
├── vite.config.js         # Vite configuration
├── public/                # Static assets served by Vite
│   └── vite.svg
├── src/                   # Frontend source code (React)
│   ├── App.jsx            # Root component with state-based page navigation
│   ├── main.jsx           # Vite React entry point
│   ├── index.css          # Global styles (Tailwind CSS directives)
│   ├── components/        # Reusable React components
│   │   ├── Header.jsx     # Top navigation bar (Home / About)
│   │   ├── UploadArea.jsx # Input panel (text, screenshot, Figma URL)
│   │   ├── CodeEditor.jsx # Generated code display with copy button
│   │   └── ResultDisplay.jsx # Loading / error / result wrapper
│   ├── pages/             # Page-level components
│   │   ├── HomePage.jsx   # Main conversion page
│   │   └── AboutPage.jsx  # About page
│   └── utils/
│       └── api.js         # Fetch helpers for all three backend endpoints
└── server/                # Backend source code (Flask)
    ├── app.py             # Flask app entry point; registers blueprints
    ├── download_model.py  # Utility to download Salesforce/codegen-350M-mono locally
    ├── routes/            # Blueprint route handlers
    │   ├── __init__.py
    │   ├── text_to_code.py        # POST /api/text-to-code
    │   ├── screenshot_to_code.py  # POST /api/screenshot-to-code
    │   └── figma_to_code.py       # POST /api/figma-to-code
    ├── services/          # Business logic / AI integration
    │   ├── __init__.py
    │   ├── nlp_services.py    # Calls Colab AI endpoint; keyword fallback
    │   ├── figma_services.py  # Fetches Figma API data (placeholder conversion)
    │   └── vision_services.py # Screenshot processing (placeholder)
    └── models/            # Directory for locally downloaded model files (IGNORED by Git)
        └── __init__.py
```

## Future Enhancements

  * **Implement Screenshot to Code:** Integrate a Computer Vision model (e.g., YOLO, Mask R-CNN) for UI element detection and layout analysis.
  * **Implement Figma to Code:** Develop robust parsing logic for Figma's API data to translate design properties into precise code.
  * **Support More Code Formats:** Extend generation to React components, Vue components, etc.
  * **Live Preview:** Add a sandbox or iframe to render the generated code live.
  * **Code Refinement:** Implement code quality checks, best practices, and optimization for generated code.
  * **User Authentication:** For more advanced features or private designs.
  * **Deployment:** Deploy the frontend (e.g., Vercel, Netlify) and backend (e.g., Render, Google Cloud Run) to cloud platforms.

