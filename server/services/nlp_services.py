# server/services/nlp_service.py
import os
import torch # Used to check for GPU availability and for model loading
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# --- Global variable for the loaded model and tokenizer ---
# This will hold the text generation pipeline, loaded once when the Flask app starts.
nlp_model_pipeline = None

# Define the path where you are storing your fine-tuned model and tokenizer files.
# This should match the path where you saved the model using the download_model.py script.
# os.path.dirname(__file__) gets the current directory (services/)
# '..' goes up one level (to server/)
# 'models' enters the models directory
# 'nlp_code_generator' is the specific folder for your NLP model files.
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models', 'nlp_code_generator')

# Attempt to load the model globally when the service module is imported (i.e., when app.py starts).
# This prevents reloading the model for every API request, which would be very slow and inefficient.
try:
    if os.path.exists(MODEL_DIR) and os.path.isdir(MODEL_DIR):
        print(f"[NLP Service] Attempting to load NLP model from: {MODEL_DIR}")
        
        # Load tokenizer: Responsible for converting text to numerical tokens and vice-versa.
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        
        # Load model: This loads the actual neural network weights and architecture.
        # For small models like CodeGen-350M-mono, `device_map="auto"` might not be strictly necessary,
        # but it's good practice for larger models. `torch_dtype=torch.float16` can save memory on GPU.
        # For CPU-only, float16 is usually converted to float32 internally, so it might not offer much benefit.
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_DIR,
            # Use float16 to reduce memory usage if a GPU is available.
            # If you encounter issues on CPU, you might try removing this line or setting to torch.float32.
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, 
            device_map="auto" # Automatically determines where to load model parts (GPU/CPU)
        )

        # Determine the device (GPU if available, otherwise CPU).
        device = 0 if torch.cuda.is_available() else -1
        
        # Create a text generation pipeline: This is a high-level abstraction from Hugging Face
        # that simplifies the process of tokenization, model inference, and decoding.
        nlp_model_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=device # Assign the model to the determined device (GPU or CPU)
        )
        print("[NLP Service] NLP Model loaded successfully.")
    else:
        print(f"[NLP Service] NLP model directory not found at {MODEL_DIR}. Using placeholder logic.")
except Exception as e:
    print(f"[NLP Service] Could not load NLP model due to an error: {e}. Using placeholder logic.")
    print(f"[NLP Service] Please ensure '{MODEL_DIR}' exists and contains valid Hugging Face model files.")


def generate_code_from_text(text_description: str) -> str:
    """
    Generates HTML/CSS code from a natural language text description using an NLP model.
    """
    print(f"[NLP Service] Processing text - '{text_description}'")

    # --- Actual Model Inference Logic ---
    # This block executes if the NLP model was successfully loaded during application startup.
    if nlp_model_pipeline: 
        try:
            # Construct the prompt for the LLM.
            # For CodeGen models, prompts are often expected as comments or direct instructions.
            # The more explicit you are, the better, even for small models.
            # Example prompt for CodeGen-350M-mono for Python: "def hello_world():"
            # For HTML/CSS, we need to guide it more.
            prompt = f"# Generate HTML and Tailwind CSS for the following UI description:\n# Description: {text_description}\n\n"
            # Add a hint for the expected output format
            prompt += "```html\n" 

            # Generate code using the loaded pipeline
            # Adjust generation parameters for optimal results with this specific model.
            # - max_new_tokens: Maximum number of tokens (words/subwords) to generate.
            #   Adjust based on typical code length you expect. 768 is a reasonable upper limit.
            # - num_return_sequences: Number of different outputs to generate (usually 1 for simplicity).
            # - do_sample: If True, uses sampling for more diverse outputs (vs. greedy decoding).
            # - temperature: Controls the randomness of sampling. Lower (e.g., 0.1-0.5) makes output
            #   more deterministic; higher (e.g., 0.7-1.0) makes it more creative/random.
            # - top_k: Limits sampling to the top-k most probable next tokens.
            # - top_p: Nucleus sampling; limits to tokens whose cumulative probability is less than top_p.
            # - pad_token_id: Crucial for generation to stop cleanly when the model generates its
            #   padding token (often same as EOS token).
            
            # Note: For CodeGen, its tokenizer's eos_token_id is usually 50256 (same as GPT-2).
            # We explicitly set it for clarity and robustness.
            generated_sequence = nlp_model_pipeline(
                prompt,
                max_new_tokens=768, 
                num_return_sequences=1,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                pad_token_id=nlp_model_pipeline.tokenizer.eos_token_id 
            )

            # Extract the generated text. The pipeline returns a list of dictionaries.
            full_generated_text = generated_sequence[0]['generated_text']

            # Post-process: Clean up the generated text.
            # 1. Remove the original prompt from the generated text.
            code = full_generated_text.replace(prompt, "").strip()

            # 2. Remove common markdown code block fences if the model generates them.
            # CodeGen often generates code within markdown blocks.
            if code.startswith('```html'):
                code = code[7:].strip() # Remove '```html'
                if code.endswith('```'):
                    code = code[:-3].strip() # Remove closing '```'
            elif code.startswith('```'): # Generic markdown block
                code_lines = code.split('\n')
                if len(code_lines) > 2: # Check if there's content between fences
                    code = '\n'.join(code_lines[1:-1]).strip() # Remove first and last lines

            # 3. Further refinement: CodeGen-350M-mono is Python-focused. 
            # It might generate Python comments or Python-like structures.
            # A simple heuristic to remove lines that look like Python comments or empty lines.
            code_lines = [line for line in code.split('\n') if not line.strip().startswith('#') and line.strip() != '']
            code = "\n".join(code_lines).strip()
            
            # You might want to add more sophisticated parsing/validation here,
            # e.g., using a simple HTML parser to check for well-formedness of tags.

            print(f"[NLP Service] Generated code (first 200 chars):\n{code[:200]}...")
            return code

        except Exception as e:
            print(f"[NLP Service] Error during NLP model inference: {e}")
            # If an error occurs during inference, fall back to the placeholder logic.
            pass 

    # --- Placeholder Logic (Fallback if model not loaded or inference fails) ---
    # This section will be executed if the NLP model failed to load during startup,
    # or if an error occurred during inference (and caught above).
    text_description_lower = text_description.lower()
    if "button" in text_description_lower and "blue" in text_description_lower:
        return "<button class='bg-blue-500 text-white p-2 rounded-md shadow-md hover:bg-blue-600 transition-colors'>Blue Button</button>"
    elif "heading" in text_description_lower and "large" in text_description_lower:
        return "<h1 class='text-4xl font-bold text-gray-800 mb-4'>Large Heading</h1>"
    elif "input field" in text_description_lower:
        return "<input type='text' placeholder='Enter text...' class='border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent'>"
    elif "card" in text_description_lower:
        return """
<div class="bg-white rounded-lg shadow-lg p-6 max-w-sm mx-auto">
    <h2 class="text-xl font-semibold mb-2">Sample Card</h2>
    <p class="text-gray-600">This is a simple card component.</p>
    <button class="mt-4 bg-purple-500 text-white px-4 py-2 rounded-md hover:bg-purple-600">Learn More</button>
</div>
        """
    return f"""
<div class="p-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-md">
    <p>Placeholder for text-to-code conversion.</p>
    <p>NLP model not loaded or inference failed. Using fallback logic.</p>
    <p>Current input: "{text_description}"</p>
</div>
    """