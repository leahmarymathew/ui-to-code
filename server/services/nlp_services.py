# server/services/nlp_service.py
import os
import requests # For making HTTP requests to the Colab AI endpoint
from dotenv import load_dotenv # To load COLAB_AI_API_URL from .env

# Load environment variables (important for loading COLAB_AI_API_URL)
load_dotenv()

# Get the URL of the Colab AI inference endpoint from environment variables.
# This will be used to send text description requests to your Colab notebook.
COLAB_AI_API_URL = os.environ.get('COLAB_AI_API_URL')

if not COLAB_AI_API_URL:
    print("[NLP Service] WARNING: COLAB_AI_API_URL not set in .env. Falling back to local placeholder.")

def generate_code_from_text(text_description: str) -> str:
    """
    Generates HTML/CSS code from a natural language text description by calling the Colab AI endpoint.
    """
    print(f"[NLP Service] Processing text - '{text_description}'")

    # --- Call Colab AI Endpoint ---
    # This block executes if COLAB_AI_API_URL is set in your .env file.
    if COLAB_AI_API_URL:
        try:
            # Prepare the payload for the Colab AI endpoint.
            payload = {"text": text_description}
            
            # Make a POST request to the Colab AI endpoint.
            # Set a generous timeout (e.g., 120 seconds) as Colab inference can still take time,
            # especially for larger models or if the Colab instance is just warming up.
            response = requests.post(COLAB_AI_API_URL, json=payload, timeout=120) # 120-second timeout

            # Raise an HTTPError for bad responses (4xx or 5xx status codes).
            response.raise_for_status() 

            # Parse the JSON response from the Colab AI endpoint.
            colab_response_data = response.json()

            # Check if the response contains the 'code' field (success).
            if "code" in colab_response_data:
                generated_code = colab_response_data["code"]
                print(f"[NLP Service] Generated code (first 200 chars from Colab):\n{generated_code[:200]}...")
                return generated_code
            # Check if the response contains an 'error' field.
            elif "error" in colab_response_data:
                error_msg = colab_response_data.get("message", colab_response_data["error"])
                details = colab_response_data.get("details", "No further details.")
                print(f"[NLP Service] Error from Colab AI: {error_msg} - Details: {details}")
                # Re-raise as a generic Exception to be caught by the outer except block,
                # ensuring a consistent error HTML is returned.
                raise Exception(f"Colab AI Error: {error_msg} ({details})")
            # Handle unexpected response formats from the Colab AI endpoint.
            else:
                raise Exception("Unexpected response format from Colab AI.")

        # --- Error Handling for requests to Colab AI Endpoint ---

        # Handles cases where the request times out.
        except requests.exceptions.Timeout:
            print("[NLP Service] Colab AI request timed out.")
            return f"""
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error: AI conversion timed out. Colab might be too slow or disconnected.</p>
    <p>Please check the Colab notebook and try again.</p>
</div>
            """
        # Handles network-related errors (e.g., Colab server down, ngrok not running).
        except requests.exceptions.ConnectionError:
            print("[NLP Service] Could not connect to Colab AI endpoint. Is ngrok running and URL correct?")
            return f"""
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error: Could not connect to Colab AI endpoint. Ensure your Colab notebook is running and ngrok is active.</p>
</div>
            """
        # Handles other HTTP-related errors (e.g., 4xx, 5xx responses from Colab Flask app).
        except requests.exceptions.RequestException as e:
            print(f"[NLP Service] Request error to Colab AI: {e}")
            return f"""
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error: Failed to get response from Colab AI: {str(e)}</p>
    <p>Check Colab notebook output for details.</p>
</div>
            """
        # Catches any other unexpected errors during the process.
        except Exception as e:
            print(f"[NLP Service] Unexpected error in Colab AI call: {e}")
            return f"""
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error: An unexpected error occurred during AI conversion: {str(e)}</p>
</div>
            """
    # --- Fallback to Local Placeholder ---
    # This block executes if COLAB_AI_API_URL is NOT set (meaning you want to use local inference),
    # or if any of the exceptions above occurred during the call to the Colab AI endpoint.
    else:
        print("[NLP Service] COLAB_AI_API_URL not set or Colab call failed. Using local placeholder logic.")

        # Your original local placeholder logic (as defined in previous steps).
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
    <p>Fallback: AI model not available or call failed.</p>
    <p>Current input: "{text_description}"</p>
</div>
        """