from flask import Flask, request, jsonify
import requests
import configparser

import vertexai
from vertexai.language_models import TextGenerationModel

import google.auth
from google.auth.exceptions import DefaultCredentialsError


# Create a Flask application
app = Flask(__name__)

# Define a route and a function to handle requests


def _get_information_context():
    with open('./data/resource_catalog.txt', 'r') as file:
        information_context = file.read()

    return information_context 


def _prompt_adjustment(user_input, information_context):
    structured_prompt = f"""
    You are a Language Model specializing in discovering existing resources. Below is the user's input and a list of hospital resources to help you identify the resource the user is looking for.

    **User Input**: {user_input}

    **Information Context**:
    {information_context}

    Please provide the answer as a title, type, and description of the resource.
    Do not invent any resources that are not present in the information context.
    """

    return structured_prompt


def _process_response(resp):
    if resp is not None:
        content = resp['predictions'][0]['content']
        return content
    
    generated_text = "unfortunately, LLM service is down right now"
    return generated_text


def _call_LLM(prompt, temperature, top_p, top_k):
    '''
    # [ Alternative Code ]
    # config = configparser.ConfigParser()
    # config.read('config.ini')

    # LLM_service_endpoint = config['LLM']['url']

    # headers = {
    #     "Authorization": f"Bearer {config['Headers']['authorization']}"
    # }

    # payload = {
    #     "instances": [
    #         { "prompt": prompt }
    #     ],
    #     "parameters": {
    #         "temperature":temperature,
    #         "maxOutputTokens":2048,
    #         "topK":top_k,
    #         "topP":top_p
    #     }
    # }

    # response = requests.post(
    #     LLM_service_endpoint,
    #     headers=headers,
    #     json=payload
    # )
    '''

    try:
        credentials, project = google.auth.default()
        vertexai.init(credentials=credentials, project=project, location="us-central1")
        
        parameters = {
            "candidate_count": 1,
            "max_output_tokens": 2048,
            "temperature": temperature,
            "top_p": top_p
        }

        model = TextGenerationModel.from_pretrained("text-bison")
        response = model.predict(prompt, **parameters)
        print(response)

        if not response.text:
            raise Exception(f"Request failed with status {response.text}")
        
        # response_json = response.json()
        # processed_response = _process_response(response_json)
        processed_response = response.text

        return '### Use-Case 1: Resource Discovery\n\n' + processed_response

    except DefaultCredentialsError:
        raise Exception("Google Cloud credentials not found. Please ensure GOOGLE_APPLICATION_CREDENTIALS is set.")

    except Exception as e:
        raise Exception(f"Error calling Vertex AI: {e}")


    
@app.route('/')
def hello_world():
    return '<h1>Use-Case #1  - Resource Discovery </h1>'


@app.route('/post', methods=['POST'])
def post_message():
    # Check if request contains JSON data
    if request.is_json:
        data = request.json
        user_input = data.get('message')
        if user_input:
            response = {
                'status': 'success',
                'message_received': user_input
            }

            # [ DEMO CODE HERE ]

            # step 1: get neccessary context for structuring prompt 
            # ! [ IF CONTEXT TOO LARGE ] - Need Vector Database (or Vertex AI Search)
            information_context = _get_information_context()

            # step 2: get structured prompt to call LLM
            structured_prompt = _prompt_adjustment(user_input, information_context)

            # step 3: call LLM
            temperature = 0.7
            top_p = 0.95
            top_k = 40
            response = _call_LLM(structured_prompt,temperature, top_p, top_k)

            # step 4: refering other services (not provided in this demo)
            # pass

            return jsonify(response), 200
        else:
            return jsonify({'error': 'Message not provided'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 400



# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
