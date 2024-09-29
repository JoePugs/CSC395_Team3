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


initial_context = '''
You are an expert chef!  Given the ingredients and name brand, you make a recipe that works!
'''
def getRecipe(context, ingredients, brand):
    # Your logic to call Ollama or generate a recipe
    ollama_reply = generate_ollama_response(context, ingredients)
    response_data = {'success': True, 'ollama_reply': ollama_reply, 'reply': ollama_reply}
    return response_data

def generate_ollama_response(content,question):
    client = Client(host='http://localhost:11434')
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
        
        # Get JSON data from the request
        data = request.get_json()
        
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
        else:
            logger.info("One shot to correct the failing code:")
            logger.info(response_data['ollama_reply'])
            logger.info(response_data)
        
        # Return the response data as JSON
        return jsonify(response_data)
    
    except Exception as e:
        logger.info("An exception has occurred")
        tb = e.__traceback__
        file_name, line_number = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        logger.info(f"\tError occurred in: {file_name} at line {line_number}")
        
        # Log and return the error message
        error_message = str(e)
        logger.info(error_message)
        
        # Ensure ollama_reply is always defined
        response_data = {'success': False, 'error': error_message, 'ollama_reply': ollama_reply or "No reply"}
        return jsonify(response_data), 500
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
