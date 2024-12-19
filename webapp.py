from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Replace these with your actual API key and character ID
API_KEY = "0c4d8e49f1244043408a7cced81993aa"
CHARACTER_ID = "32a6a8bc-b656-11ef-b082-42010a7be016"
SESSION_ID = -1  # Default session ID for new sessions

def send_request(api_key, character_id, session_id, user_input=None):
    """
    Sends a request to the Conva.ai API with text input.

    :param api_key: Your API key for authentication
    :param character_id: The character ID for the interaction
    :param session_id: The session ID (-1 for new session)
    :param user_input: Text input from the user
    :return: Character response text
    """
    url = "https://api.convai.com/character/getResponse"

    headers = {
        "CONVAI-API-KEY": api_key
    }

    payload = {
        "userText": user_input,
        "charID": character_id,
        "sessionID": session_id,
        "voiceResponse": "false"  # Ensure no audio is requested
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json().get("text", "No response available.")
    else:
        return "Error: Failed to get response from API."

@app.route("/")
def home():
    return "Flask server is running!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No user input provided."}), 400

    try:
        response_text = send_request(API_KEY, CHARACTER_ID, SESSION_ID, user_input)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
