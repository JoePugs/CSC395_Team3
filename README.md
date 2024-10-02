# CSC395_Team3
### AI-Generated Recipe Developer ###
Learn how to master the kitchen! This is a web browser application that makes cooking at home easy and fun! Just input the food brand you want to incorporate and your avaliable ingredients, and the application will output an AI-generated delicious recipe with simple instructions. Happy Cooking!


### Pre-Reqs ###
To run the Recipe Developer application, you will need to install a Docker Engine on your local machine. Once install, run the docker from the terminal with this command: 

 ```docker-compose up```  
 and to stop running it, issue this command:  
 ```docker-compose down```

Once you have the Docker installed, you need to pull the Ollama image using this command:  
```docker pull ollama/ollama```  
Important note: Your machine needs to have at least 16MG to the Ollama API. Otherwise, your machine will run out of RAM and proper installing won't occur.   
To run the Ollama Docker container, use this command next:  
```docker run -p 11434:11434 ollama/ollama```

Next, you need to install the Flask in order to run the Python web framework that will handle the API.
Use this command in the terminal:  
```pip install flask```
Make sure you also have a Python IDE version of model 3 or higher. Visual Studios would be an example environment in which the code could run from. 


### Framework Description ### 
The AI-Generated Recipe Developer runs on two containers noted in the ```docker-compose.yml``` file--the Python Flask and Ollama.   

**Python Flask:**
The entry point for the Flask server is the file ```app.py``` found in the main branch at the root directory.  
Key Elements of the Flask:  
    1. Receives user input from UI (brand name and ingredients).  
    2. Sends this input as a JSON message to the Ollama API.  
    3. Receives the Ollama reply (user's recipe).  
    4. Sends Ollama's recipe output back to the UI to be displayed.  
The Flask server is responsible for inputting the user's request to the API and also ensuring the API's reply gets back to the UI for the user to see. Think of the Flask as the median where it is responsible for ensuring the data is sent to the correct systems.  

**Ollama**  
The Ollama container is utilizes the Large Language Models (LLM) to generate responses based on the user's input. The Ollama API produces raw code in which the Flask server interprets as readable language and sends back to the UI. The Ollama container is capable of running different LLMs depending on what which is specified in the ```pull``` command.  
Important Notes:  
The Ollama container was initially using the LLM called ```codellama``` which was installed locally. Ensure this (or any LLM) is installed on your local machine using this command:  
```ollama pull codellama```  


### Application Use ###
The docker-compose.yml file utilizes port 5000 on your local machine in order for the web browser to connect with the Flask server. The diagram below maps out the system's architecture:  

![Screenshot]("./images/Screenshot.png")  













