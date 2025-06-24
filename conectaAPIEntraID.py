# This script connects to EntraID (Azure Active Directory) using the MSAL library
# and retrieves an access token to make API calls to Microsoft Graph.

# uses the following libraries:
# - os: to access environment variables
# - dotenv: to load environment variables from a .env file
# - requests: to make HTTP requests to the Microsoft Graph API
# - msal: to handle authentication with Microsoft EntraID

# by Flavio Brandão

import os
from dotenv import load_dotenv
import requests
from msal import ConfidentialClientApplication

# Load env decrypted file for the parameters
# This file should be created using the encrypt_env.py script
load_dotenv('.env.decrypted')

#Parameters for EntraID connection
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')

AUTHORITY = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
SCOPE = ['https://graph.microsoft.com/.default']

# Initialize connection
#the app receives the tuple (client_id, client_secret, authority)

app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

# Obtain token 
# The if is a boolean expression that checks 
# if the access_token is in the result

result = app.acquire_token_for_client(scopes=SCOPE)

# the result is a dictionary that contains the access_token and other information
# if the access_token is not in the result, the authentication failed 
# if the access_token is in the result, the authentication was successful

if "access_token" in result:
    print("Connection with EntraID established")

    # url Test simple API call
    # This call is used to test if the connection is working 
    url = 'https://graph.microsoft.com/v1.0/users?$top=1'
    headers = {
        'Authorization': 'Bearer {}'.format(result['access_token'])
    }
# respose gets the response from the API call
    response = requests.get(url, headers=headers)

# if "response" gets the status code 200 so the API call was successful
# if the "response" gets a different status code the API call failed 

    if response.status_code == 200:
        print("API Call succeed")
    else:
        print("Fail on the API call: {} - {}".format(response.status_code, response.text))
# last else for access_token not in result
# for k and v stands for key and value in the result dictionary
# this prints the details of the authentication result
    
else:
    print("Authentication Failed")
    print("Details:")
    for k, v in result.items():
        print("{}: {}".format(k, v))