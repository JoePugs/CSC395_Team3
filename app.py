from flask import Flask, jsonify, request, render_template, send_file, url_for
import datetime
from ollama import Client
import os
import importlib
import secrets
import logging
import black
import sys
import io

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
if False:  # Replace this with a condition that determines when to print messages to the console
    console_handler.setLevel(logging.DEBUG)
else:
    console_handler.setLevel(logging.CRITICAL)
app = Flask(__name__)


# Dictionary to store the imported functions and their respective keys
function_registry = {}

initial_context = '''
You take the instructions provided and generate a runnable Python function.
new_function must be the name of the entry method for the code you create.
You must add all imports you know will be needed.
You must only provide Python code and cannot include descriptions of the code. 
The code you return will be used immediately so
it must work. Do not, under any circumstances, add anything in 
your reply that is not python code.  Add absolutely no comments - none!
Also, pay particular attention to modules used and the imports needed.  It is
absolutely imperative you import all the modules needed at top.  No exceptions!
You must review the indentation used and ensure it is absolutely perfect.  No exceptions
otherwise the code will not compile. Any exceptions should be raised and sent to the function that
will call new_function. The code that calls new_function will catch and handle
the raised exception. Do not explain the code at all.  Just return the Ptyhon code only.  Do
not incldue an explanation of what the code is doing.
'''

def register(key, module):
    """Registers a dynamically imported function with its corresponding key."""
    function_registry[key] = getattr(module, key)

def invoke(key, *args, **kwargs):
    """Invokes a registered function using its key and passes the provided arguments."""
    if key in function_registry:
        result = function_registry[key](args, kwargs)
        return result
    else:
        raise KeyError(f"Function with key '{key}' not found.")

def remove_first_and_last_lines(multiline_string):
    multiline_string = multiline_string.replace("```","")
    lines = multiline_string.split('\n')  # Split the string into lines using newline character as delimiter
    return '\n'.join(lines[1:-1])  # Join all but the first and last lines back together with a newline character

def create_persisted_code(generated_code, random_prefix):

    if not os.path.exists('temp'):
        os.makedirs('temp')

    # Write the generated code to a file
    with open(os.path.join('temp', f'{random_prefix}.py'), 'w') as f:
        f.write(generated_code)
    #logger.info(f'The generated code is: {generated_code}')

    # Construct the fully qualified module name
    module_name = f'temp.{random_prefix}'

    # Import the module dynamically
    try:
        new_module = importlib.import_module(module_name)
        logger.info(f'{module_name} successfully imported')
        #register(random_prefix, new_module)
        return new_module
    except ImportError:
        logger.error(f'Error importing {module_name}')

def register(random_prefix, new_module, new_param):
    try:
        result = new_module.new_function(new_param)
        logger.info("Function call successful")
        logger.info("Result: ", result)
    except Exception as e:
        logger.info("Error while calling the function: " + str(e))
        tb = e.__traceback__
        file_name, line_number = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        logger.info(f"\tError occurred in: {file_name} at line {line_number}")

def generate_ollama_response(content,question):
    client = Client(host='http://host.docker.internal:11434')
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


# Ollama API URL
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434/api/chat")

# Define a route to serve the index.html file from the same directory as app.py
@app.route('/')
def serve_index():
    print("Called index")
    logger.error("ERROR")
    logger.info("THIS WORKS")
    return render_template('index.html')

# Define a route that accepts POST requests and handles JSON data
@app.route('/process', methods=['OPTIONS', 'POST'])
def process():
    try:
        logger.info('Accessing json message')
        data = request.get_json()
        ingredients = data['ingredients']
        brand = data['brand']
        logger.info('Json message processed')

        logger.info(f"Received JSON data: {data}")
        logger.info(f"Ingredients: {ingredients}")
        logger.info(f"Brand: {brand}")

        logger.info("About to call callNewlyGeneratedCode")
        response_data = callNewlyGeneratedCode(initial_context, ingredients, brand)
        if response_data['success']:
            logger.info("We have a successful compilation and execution!")
            logger.info("Here is the answer")
            logger.info(response_data['reply'])
        else:
            logger.info("One shot to correct the failing code:")
            logger.info(response_data['ollama_reply'])
            #one_shot_context = get_one_shot_context(response_data)
            #logger.info(one_shot_context)
            #response_data = callNewlyGeneratedCode(one_shot_context, response_data['ollama_reply'], input)
            #logger.info(response_data)
            logger.info(">>>>----------------------")
            logger.info(response_data)
        print("Counting finished.")
        return jsonify(response_data)
    except Exception as e:
        logger.info("An exception has occurred")
        tb = e.__traceback__
        file_name, line_number = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        logger.info(f"\tError occurred in: {file_name} at line {line_number}")
        error_message = str(e)
        logger.info(error_message)
        response_data = {'success': False, 'error': error_message, 'ollama_reply': ollama_reply}
        return jsonify(response_data), 500 
    
def get_one_shot_context(response_data):
    context = f'''
                Look at this failing code.  Correct it based on this error message 
                enclosed in parenthesis:
                ({response_data['error']}.)
                new_function must be the name of the entry method for the code you create.
                You must add all imports you know will be needed.
                You must only provide Python code in your reply and cannot include descriptions of the code. 
                The code you return will be used immediately so
                it must work. Do not, under any circumstances, add anything in 
                your reply that is not python code.  Add absolutely no comments - none!
                Again, do not add any comments to the code you generate.  None.
                Also, pay particular attention to modules used and the imports needed.  
                Again, you are only to return in your reply python code - return absolutely
                nothing else than python code. Any exceptions should be raised and sent to the function that
                will call new_function. The code that calls new_function will catch and handle
                the raised exception.
                '''
    return context
    

def callNewlyGeneratedCode(context, ingredients, brand):
    logger.info("First line of callNewlyGeneratedCode")
    try:
        # Perform some logic or validation here based on your use case
        ollama_reply = generate_ollama_response(context, ingredients)
        logger.info(f"Here is the ollama reply before removing first and last lines {ollama_reply}")
        ollama_reply = remove_first_and_last_lines(ollama_reply)
        logger.info(f"Here is the ollama_reply after removing first and last lines {ollama_reply}")
        ollama_reply = black.format_str(ollama_reply, mode=black.FileMode())
        logger.info("From within callNewlyGeneratedCode here is the ollama_reply")
        logger.info(ollama_reply)
        # Generate a random prefix for the filename
        random_prefix = str(secrets.token_bytes(8).hex())
        new_module = create_persisted_code(ollama_reply, random_prefix)
        #reply = new_module.new_function(input)
        if brand is None or len(brand) == 0:
            new_function = new_module.new_function  # Assuming 'some_module' has been imported previously
            reply = new_function()
        else:
            reply = new_module.new_function(brand)
        logger.info(reply)
        response_data = {'success': True, 'ollama_reply': ollama_reply, 'reply': reply}
        #return jsonify(response_data)
        return response_data
    except Exception as e:
        logger.info("An exception has occurred")
        tb = e.__traceback__
        file_name, line_number = tb.tb_frame.f_code.co_filename, tb.tb_lineno
        logger.info(f"\tError occurred in: {file_name} at line {line_number}")
        error_message = str(e)
        logger.info(error_message)
        response_data = {'success': False, 'error': error_message, 'ollama_reply': ollama_reply}
        #return jsonify(response_data), 500
        return response_data
    

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
