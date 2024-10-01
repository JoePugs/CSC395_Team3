from flask import Flask, jsonify, request, render_template, send_file, url_for
import datetime
from ollama import Client
import os
import importlib
import secrets
from flask_cors import CORS
import logging
import sys
import io
import black
#Start
# Create a custom logger
logger = logging.getLogger(__name__)

# Set the level for the logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logger.setLevel(logging.INFO)

# Define handlers for the log messages
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app.log')

# Set formatters for the log messages
formatter = logging.Formatter('%(asctime)s %(name)s:%(lineno)d %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger and enable/disable them as required
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Enable logging to console and disable it for file
#if False:  # Replace this with a condition that determines when to print messages to the console
#    console_handler.setLevel(logging.DEBUG)
#else:
#    console_handler.setLevel(logging.CRITICAL)
app = Flask(__name__)

CORS(app)

<<<<<<< HEAD
=======

>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598

initial_context = '''
You are an expert chef!  Given the ingredients and brand given, you make a recipe that works! You MUST include a product from the brand to you along with the ingredients!
'''
def getRecipe(context, ingredients, brand):
    # Your logic to call Ollama or generate a recipe
    question = f"Ingredients: {ingredients}. Brand: {brand}."
    ollama_reply = generate_ollama_response(context, question)
    response_data = {'success': True, 'ollama_reply': ollama_reply, 'reply': ollama_reply}
    return response_data

def generate_ollama_response(content,question):
<<<<<<< HEAD
    client = Client(host='http://localhost:11434')
=======
    client = Client(host='http://localhost:11434')   # Port matches the docker-compose file. Verifying Flask and Ollama are operating on same port. 
>>>>>>> 93e588febbaa72fcfd2eb866aec6e845dbe32598
    stream = client.chat(model='codellama', messages=[
    {"role": "system", "content": content},
    {"role": "user", "content": question}
    ],stream=True)
    full_answer = ''
    for chunk in stream:
        full_answer =''.join([full_answer,chunk['message']['content']])
    #logger.info(full_answer)
    #logger.info(f'Full code answer is: {full_answer}')
    return full_answer


# Define a route to serve the index.html file from the same directory as app.py
@app.route('/')
def serve_index():
    print("Called index")
    logger.error("ERROR")
    logger.info("THIS WORKS")
    return render_template('index.html')

# Define a route that accepts POST requests and handles JSON data
@app.route('/process', methods=['POST'])
def process():
    try:
        logger.info('Accessing json message')

        # Initialize ollama_reply to None to avoid NameError in case of exceptions
        ollama_reply = None

        # Get JSON data from the request (silent=True prevents raising an exception)
        data = request.get_json(silent=True)
        if data is None:
            raise ValueError("Malformed JSON")  # Explicitly raise an error if parsing fails

        ingredients = data['ingredients']
        brand = data['brand']
        logger.info('Json message processed')

        logger.info(f"Received JSON data: {data}")
        logger.info(f"Ingredients: {ingredients}")
        logger.info(f"Brand: {brand}")

        # Call the getRecipe function
        logger.info("About to call getRecipe")
        response_data = getRecipe(initial_context, ingredients, brand)

        if response_data['success']:
            logger.info("We have a successful compilation and execution!")
            logger.info("Here is the answer")
            logger.info(response_data['reply'])
            return jsonify(response_data), 200
        else:
            logger.info("One shot to correct the failing code:")
            logger.info(response_data['ollama_reply'])
            logger.info(response_data)
            return jsonify(response_data), 500

    except ValueError as ve:
        logger.error("Malformed JSON received: %s", str(ve))
        return jsonify({'success': False, 'error': 'Malformed JSON'}), 400  # Return 400 Bad Request

    except Exception as e:
        logger.error("An exception occurred: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/status')
def status():
    print("Fielded a status request")
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify({'message': 'All is well', 'timestamp': current_time})

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    logger.info("About to run flask server")
    app.run(host='0.0.0.0', port=5000, debug=True)
    logger.info("server is running")

    # Docker build command can be added as a comment
    # To build 
    # docker build -t csc395_team3-flask-app
    # docker-compose up
