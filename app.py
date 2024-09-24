from flask import Flask, request, jsonify, send_from_directory
import os
import requests

app = Flask(__name__)

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api"

# Define a route to serve the index.html file from the same directory as app.py
@app.route('/')
def serve_index():
    # Get the current directory
    directory = os.path.dirname(os.path.abspath(__file__))
    # Send index.html from the same directory
    return send_from_directory(directory, 'index.html')


# Define a route that accepts POST requests and handles JSON data
@app.route('/json', methods=['POST'])
def receive_json():
    # Check if the request contains JSON data
    if request.is_json:
        # Parse the incoming JSON data
        data = request.get_json()

        # Log the received data (optional)
        print(f"Received JSON data: {data}")

        try:
            # Send the JSON data (prompt) to Ollama API
            ollama_response = requests.post(
                f"{OLLAMA_API_URL}/chat",
                json={"prompt": data.get('prompt', '')}  # Assume 'prompt' is a key in the incoming JSON
            )

            # Check if the request to Ollama was successful
            if ollama_response.status_code == 200:
                ollama_response_data = ollama_response.json()
                model_output = ollama_response_data.get("response", "No response from model")

                # Create a response dictionary to send back to the client
                response = {
                    "status": "success",
                    "message": "JSON received and processed",
                    "data": data,  # Echo the received JSON back
                    "model_output": model_output  # Include Ollama's response
                }
            else:
                # If Ollama API request failed, log the error and return the failure response
                response = {
                    "status": "error",
                    "message": "Failed to connect to Ollama API",
                    "details": ollama_response.text
                }

            # Return the JSON response
            return jsonify(response), 200

        except Exception as e:
            # Catch any errors during the request and return an error response
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        # If the request does not contain JSON, return an error
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)