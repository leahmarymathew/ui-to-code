# server/routes/screenshot_to_code.py
from flask import Blueprint, request, jsonify
from server.services.vision_services import generate_code_from_screenshot
import os

# Create a Blueprint for screenshot-to-code routes
screenshot_to_code_bp = Blueprint('screenshot_to_code', __name__)

@screenshot_to_code_bp.route('/screenshot-to-code', methods=['POST'])
def screenshot_to_code():
    """
    API endpoint to convert a screenshot image to code.
    Expects a file upload with key 'image'.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # For demonstration, we'll save the image temporarily.
    # In a real application, consider direct processing or cloud storage.
    upload_folder = 'uploads' # Ensure this folder exists or create it
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    image_path = os.path.join(upload_folder, image_file.filename)
    image_file.save(image_path)

    try:
        # Call the vision service to generate code from the image
        generated_code = generate_code_from_screenshot(image_path)
        return jsonify({'code': generated_code}), 200
    except Exception as e:
        print(f"Error in screenshot-to-code conversion: {e}")
        return jsonify({'error': 'Internal server error during conversion', 'details': str(e)}), 500
    finally:
        # Clean up the temporarily saved image
        if os.path.exists(image_path):
            os.remove(image_path)