# server/routes/figma_to_code.py
from flask import Blueprint, request, jsonify
from server.services.figma_services import generate_code_from_figma

# Create a Blueprint for Figma-to-code routes
figma_to_code_bp = Blueprint('figma_to_code', __name__)

@figma_to_code_bp.route('/figma-to-code', methods=['POST'])
def figma_to_code():
    """
    API endpoint to convert a Figma URL to code.
    Expects a JSON payload with a 'url' field.
    """
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing Figma URL in request body'}), 400

    figma_url = data['url']
    try:
        # Call the Figma service to generate code
        generated_code = generate_code_from_figma(figma_url)
        return jsonify({'code': generated_code}), 200
    except ValueError as e:
        return jsonify({'error': f'Invalid Figma URL: {e}'}), 400
    except Exception as e:
        print(f"Error in Figma-to-code conversion: {e}")
        return jsonify({'error': 'Internal server error during conversion', 'details': str(e)}), 500

