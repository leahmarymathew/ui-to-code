# server/download_model.py
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch # Still useful for checking CUDA availability in nlp_service.py

# --- Configuration for the small demo model ---
MODEL_NAME = "Salesforce/codegen-350M-mono" 

# The local path where the model files will be saved.
# This matches the MODEL_DIR in server/services/nlp_service.py
LOCAL_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'nlp_code_generator')

print(f"--- Starting Model Download for {MODEL_NAME} ---")
print(f"Model will be saved to: {LOCAL_MODEL_PATH}")

# Create the directory if it doesn't exist
os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)

try:
    # Load and download the tokenizer
    print(f"\nDownloading tokenizer for {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(LOCAL_MODEL_PATH)
    print("Tokenizer downloaded and saved.")

    # Load and download the model
    print(f"\nDownloading model for {MODEL_NAME}...")

    # For very small models like this, you typically don't need advanced device_map or quantization for basic demo.
    # They can usually fit into CPU RAM.
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.save_pretrained(LOCAL_MODEL_PATH)
    print("Model downloaded and saved.")

    print(f"\n--- Download Complete! Model files are in {LOCAL_MODEL_PATH} ---")

except Exception as e:
    print(f"\n--- An error occurred during download ---")
    print(f"Error: {e}")
    print("Please ensure you have an internet connection and a Hugging Face token (if required for the model).")
    print("You can log in by running 'huggingface-cli login' in your terminal.")