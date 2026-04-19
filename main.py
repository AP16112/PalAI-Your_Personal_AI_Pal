# Here this is the main file for our project in which we will write all our important code here

#------------------------------------------------------------------------------------------------------------------------------------- 
# Project :- "PalAI" - “personal AI pal” --> Your Personal AI Assistant using Groq with OpenAI 
# Here for this project, we use GROQ LLM because OPENAI API KEY access limits reached, so that's why we are using GROQ along with OPENAI client class here 
#-------------------------------------------------------------------------------------------------------------------------------------

# Here we will use flask, so we firstly need to install it using :- pip install flask

# Here we are importing this Flask class and we will use it to create this app
# request is a module or object which is used to access the request of the client

# url_for generates the correct URL for a given function or static file.
# Instead of hardcoding paths like /static/style.css or /home, you ask Flask to build them dynamically.
# This makes your app more portable and avoids broken links when you change routes or deploy under a subpath.
# url_for(endpoint, **values)
# - endpoint → usually the name of the view function (or "static" for static files).
# - values → extra arguments like filenames or route parameters.
from flask import Flask, render_template, url_for, request, jsonify
import os
from dotenv import load_dotenv
# import os → lets you interact with the operating system, including reading environment variables.
# from dotenv import load_dotenv → loads variables from a .env file into your environment so you can access them with os.getenv().
# But firstly we need to install dotenv :- pip install dotenv here

# Now here to use OpenAI , we need to install it & then also need to import it
from openai import OpenAI
# Firstly install it using :- pip install openai

# In Flask, jsonify is a helper function that makes it easy to return JSON responses from your routes. Instead of manually building JSON strings, jsonify converts Python dictionaries (or lists) into proper JSON and sets the correct response headers (Content-Type: application/json).


# Here this is web app i.e application which will take request & give some response
app = Flask(__name__)
# app = Flask(__name__, static_folder="assets", static_url_path="/assets")
# app = Flask(__name__, static_folder="assets", static_url_path="/assets_new")
# Flask(__name__) creates a new Flask web application object.
# The __name__ variable tells Flask where to look for resources (like templates or static files). It helps Flask know the “root path” of your app.
# This app object is the central piece: it handles incoming requests and sends back responses.


# In Flask (and in HTTP generally), routes accept GET requests by default unless you explicitly allow other methods like POST. 
# GET Request :-
## Purpose: Retrieve data from the server (read‑only).
## Characteristics:
### Parameters are sent in the URL query string (/search?query=flask).
### Safe and idempotent (doesn’t change server state).
### Used for loading pages, fetching resources, etc.

# POST Request :-
## Purpose: Send data to the server (create/update).
## Characteristics:
### Data is sent in the request body (not visible in the URL).
### Used for form submissions, uploading files, sending JSON payloads.
### Can change server state (e.g., adding a new user).


load_dotenv()
api_key = os.getenv("API_KEY_GROQ")


# Now we will create the OPENAI client here to use it with Groq LLM 
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)   # here this OpenAI is the basic client class



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/ask", methods=["POST"])
def ask():
    # Now here we will write the ans_query fn logic here which we have written in jupyter lab file
    # Here inside the form, our input tag must have the name="question only", otherwise this will give error
    question = request.form.get("question")
        
    response = client.responses.create(
        model="llama-3.3-70b-versatile",
        input=[
            {"role": "system", "content": "Act like a helpful personal AI assistant or pal"},                   {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_output_tokens=512
    )
        
    # here the response will be the text response
    answer = response.output_text.strip()
        
    # Flask route response that returns JSON data along with an explicit HTTP status code.
    # Converts the Python dictionary {"response": answer} into a proper JSON response.
    # This sets the HTTP status code to 200 OK (the default success code).
    return jsonify({"response": answer}), 200



@app.route("/summarize", methods=["POST"])
def summarize():
    # Now here we will write the summarize_email fn logic here which we have written in jupyter lab file
    # Here inside the form, our input tag must have the name="email" only, otherwise this will give error
    email_text = request.form.get("email")    # here we are taking the user input
    prompt = f"summarize the following email in 2-3 sentences: {email_text}"
        
    response = client.responses.create(
        model="llama-3.3-70b-versatile",
        input=[
            {"role": "system", "content": "Act like an expert email assistant"},   
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_output_tokens=512
    )

    # here the response will be the text response
    summary = response.output_text.strip()
        
    # Flask route response that returns JSON data along with an explicit HTTP status code.
    # Converts the Python dictionary {"response": summary} into a proper JSON response.
    # This sets the HTTP status code to 200 OK (the default success code).
    return jsonify({"response": summary}), 200



# standard way to run a Flask app safely.
if __name__ == "__main__":
    app.run(debug=True)
    # This line starts the Flask development server.
    # By default, Flask runs on http://127.0.0.1:5000/ (localhost, port 5000). 
    # Once you run this, Flask begins listening for incoming HTTP requests.

# debug=True Flag :-
# - Debug mode is a special setting for development:
# - Auto-reload: If you change your code and save, Flask automatically restarts the server. You don’t need to stop and restart manually.
# - Detailed error pages: If something goes wrong, Flask shows a helpful debugger in the browser with stack traces and variable inspection.
# - This makes development faster and easier, but it should not be used in production because:
# - It exposes sensitive information in error pages.
# - It can allow arbitrary code execution if misused.

# In Python, every file has a special private variable called __name__.
# If you run a file directly (like python app.py), then __name__ is set to "__main__".
# If the file is imported into another script (e.g., for testing or as part of a bigger project), then __name__ is set to the module’s name (like "app").
# This check ensures that the server only starts when you run the file directly, not when it’s imported elsewhere.

# Why This Matters :-
# - Without this guard, if another script imports your Flask app, it would immediately start the server, which is usually not what you want.
# - With the guard, you can safely import app into other files (for testing, WSGI deployment, etc.) without triggering app.run().

# Now we can run this file using :- python main.py

# SO now we can run the flask app using :-
# python main.py
# ----------OR--------
# flask --app main run --debug

