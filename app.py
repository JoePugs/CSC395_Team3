from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Ollama API URL
OLLAMA_API_URL = "http://localhost:11434/api"

# Define a route that accepts POST requests and handles JSON data
@app.route('/json', methods=['POST'])
def receive_json():
    # Check if the request contains JSON data
    if request.is_json:
        # Parse the incoming JSON data
        data = request.get_json()

        # Process the JSON data (e.g., print it)
        print(f"Received JSON data: {data}")

        # Example: Send the JSON data to Ollama API as a prompt
        ollama_response = requests.post(
            f"{OLLAMA_API_URL}/chat",
            json={"prompt": data.get('prompt', '')}  # Assume 'prompt' is a key in the incoming JSON
        )

        # Get Ollama's response
        ollama_response_data = ollama_response.json()
        model_output = ollama_response_data.get("response", "No response from model")

        # Create a response dictionary
        response = {
            "status": "success",
            "message": "JSON received and processed",
            "data": data,  # Echo the received JSON back
            "model_output": model_output  # Include Ollama's response
        }

        # Return a JSON response
        return jsonify(response), 200
    else:
        # If the request does not contain JSON, return an error
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
