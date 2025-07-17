# server/routes/text_to_code.py
from flask import Blueprint, request, jsonify
from server.services.nlp_services import generate_code_from_text

# Create a Blueprint for text-to-code routes
text_to_code_bp = Blueprint('text_to_code', __name__)

@text_to_code_bp.route('/text-to-code', methods=['POST'])
def text_to_code():
    """
    API endpoint to convert natural language text to code.
    Expects a JSON payload with a 'text' field.
    """
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text in request body'}), 400

    text_description = data['text']
    try:
        # Call the NLP service to generate code
        generated_code = generate_code_from_text(text_description)
        return jsonify({'code': generated_code}), 200
    except Exception as e:
        # Basic error handling
        print(f"Error in text-to-code conversion: {e}")
        return jsonify({'error': 'Internal server error during conversion', 'details': str(e)}), 500
