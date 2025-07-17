# server/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes, allowing your frontend to connect
CORS(app)

# Import and register blueprints/routes from the routes directory
# These files will be created next
from server.routes.text_to_code import text_to_code_bp
from server.routes.screenshot_to_code import screenshot_to_code_bp
from server.routes.figma_to_code import figma_to_code_bp

app.register_blueprint(text_to_code_bp, url_prefix='/api')
app.register_blueprint(screenshot_to_code_bp, url_prefix='/api')
app.register_blueprint(figma_to_code_bp, url_prefix='/api')

@app.route('/')
def home():
    """Basic route to confirm backend is running."""
    return "Code Converter Backend is running!"

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    # Run the Flask application
    # debug=True enables reloader and debugger, useful for development
    app.run(debug=True, port=port)