###TEST FLASK###

from flask import Flask, request, jsonify, render_template, send_file, url_for
import datetime
from ollama import Client
import os
import secrets
import logging
import black
import sys
import io


app = Flask(__name__)

# Define a route that accepts POST requests and handles JSON data
@app.route('/json', methods=['POST'])
def receive_json():
    # Check if the request contains JSON data
    if request.is_json:
        # Parse the incoming JSON data
        data = request.get_json()
        
        # Process the JSON data as needed (e.g., print it)
        print(f"Received JSON data: {data}")

        # Create a response dictionary
        response = {
            "status": "success",
            "message": "JSON received",
            "data": data  # Echo the received JSON back
        }

        # Return a JSON response
        return jsonify(response), 200
    else:
        # If the request does not contain JSON, return an error
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)


'''
    Ollama and docker connections not included yet
    Need to sort out the Json string sent from the webpage
'''