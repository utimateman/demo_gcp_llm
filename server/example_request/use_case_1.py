import requests
import json

# URL of your Flask application endpoint
url = 'http://localhost:5000/post'

# JSON payload to send in the POST request
payload = {'message': 'Is there any information about schedule of the staff'}

# Set the content type header
headers = {'Content-Type': 'application/json'}

# Send POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response from Flask application
print(response.json())
