# server/services/figma_service.py
# This file will contain the logic for interacting with the Figma API
# and translating Figma data into code.
# For now, it's a placeholder.
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Ensure environment variables are loaded here too if this file is run independently

FPGMA_API_KEY = os.environ.get('FPGMA_API_KEY')
FIGMA_API_BASE = "https://api.figma.com/v1/files/"

def get_figma_file_id(figma_url: str) -> str:
    """
    Extracts the Figma file ID from a given Figma URL.
    Example URL: https://www.figma.com/file/FILE_ID/PROJECT_NAME
    """
    parts = figma_url.split('/')
    if len(parts) > 5 and parts[4] == 'file':
        return parts[5]
    raise ValueError("Invalid Figma URL format. Expected format: https://www.figma.com/file/FILE_ID/...")

def fetch_figma_data(figma_url: str) -> dict:
    """
    Fetches design data from the Figma API for a given Figma URL.
    Requires FPGMA_API_KEY to be set in environment variables.
    """
    if not FPGMA_API_KEY:
        raise ValueError("Figma API Key (FPGMA_API_KEY) not set in environment variables.")

    file_id = get_figma_file_id(figma_url)
    headers = {"X-Figma-Token": FPGMA_API_KEY}
    api_url = f"{FIGMA_API_BASE}{file_id}"

    print(f"Figma Service: Fetching data from {api_url}")
    response = requests.get(api_url, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
    return response.json()

def generate_code_from_figma(figma_url: str) -> str:
    """
    Generates HTML/CSS code from Figma design data.
    This is a complex process involving parsing Figma's JSON structure
    and mapping design properties to code.
    """
    print(f"Figma Service: Processing Figma URL - '{figma_url}'")
    try:
        figma_data = fetch_figma_data(figma_url)
        # --- Placeholder Logic ---
        # In a real scenario:
        # 1. Recursively traverse figma_data['document']['children']
        # 2. For each node (e.g., RECTANGLE, TEXT, FRAME):
        #    a. Determine the appropriate HTML tag (div, p, h1, img, button etc.)
        #    b. Extract styling properties (fills, strokes, effects, font, layout constraints).
        #    c. Convert Figma's layout properties (x, y, width, height, constraints)
        #       into CSS (e.g., flexbox, grid, absolute positioning, responsive classes).
        #    d. Handle components, instances, and text content.
        # 3. Assemble the HTML and CSS.

        # For now, we'll just return a placeholder indicating success
        return f"""
<!-- Generated HTML for Figma URL: {figma_url} -->
<div class="p-4 bg-blue-100 border border-blue-400 text-blue-700 rounded-md">
    <p>Placeholder for Figma-to-code conversion.</p>
    <p>Figma data successfully fetched for: <strong>{figma_url}</strong></p>
    <p>Now, implement the logic to parse the Figma JSON and generate code.</p>
</div>
        """
    except ValueError as e:
        return f"""
<!-- Error during Figma conversion -->
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error: Invalid Figma URL or API Key issue.</p>
    <p>Details: {e}</p>
</div>
        """
    except requests.exceptions.RequestException as e:
        return f"""
<!-- Error during Figma API request -->
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>Error connecting to Figma API. Check URL or network.</p>
    <p>Details: {e}</p>
</div>
        """
    except Exception as e:
        return f"""
<!-- Unexpected error during Figma conversion -->
<div class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
    <p>An unexpected error occurred during Figma conversion.</p>
    <p>Details: {e}</p>
</div>
        """