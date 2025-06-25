# This script checks for inactive users in Microsoft Entra ID (Azure AD) based on the last sign-in activity.
# It retrieves users who are disabled and checks their last sign-in date against a specified threshold of
# inactivity days. If the last sign-in date is older than the threshold, it prints the user's display name and UPN.
# If the last sign-in date is not available, it indicates that the user has never signed

# by Flavio Brandão

#uses the following libraries:
# - os: to access environment variables
# - dotenv: to load environment variables from a .env file 
# - requests: to make HTTP requests to the Microsoft Graph API
# - datetime: to handle date and time operations
# - msal: to handle authentication with Microsoft Entra ID importing confidential client application
# which stands for Microsoft Authentication Library
# - sys: to handle system-specific parameters and functions
import os   
from dotenv import load_dotenv
import requests
import datetime
from msal import ConfidentialClientApplication
import sys

# load environment variables from .env files
# .env.decrypted contains the access keys
# parametros.env contains additional parameters
# the .env.decrypted file should be created using the encrypt_env.py script

# load_dotenv(".env") reads the decrypted env file
# the env file constains
# CLIENT_ID, CLIENT_SECRET, TENANT_ID, DIAS_INATIVIDADE
# DIAS_INATIVIDADE is the number of days of inactivity to filter users

load_dotenv(".env.decrypted") #decrypted env file with access keys
load_dotenv("parametros.env") #parameters file with additional parameters

# access keys from the env decrypted file
# using os.getenv with the key name passing the key name as a string
# CLIENT_ID, CLIENT_SECRET, TENANT_ID, DIAS_INATIVIDADE
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
DIAS_INATIVIDADE = os.getenv('DIAS_INATIVIDADE')

#passar o valor de parametros.env para uma string

try:
    inactive_days = int(DIAS_INATIVIDADE)
except (ValueError,TypeError):    
    print ("Inactive Days parameter is invalid").exit(1)

#login no Tenant

AUTHORITY = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
SCOPE = ['https://graph.microsoft.com/.default']

# Inicializar conexão
app = ConfidentialClientApplication(
    client_id=CLIENT_ID,
    client_credential=CLIENT_SECRET,
    authority=AUTHORITY
)

# Obter token
result = app.acquire_token_for_client(scopes=SCOPE)

if "access_token" not in result:
        print("Authentication failed")
        for k,v in result.items():
            print ("{}: {}".format(k,v)) 
            exit(1)
print ("connectio sucessful on EntraID")
print ("Scopes conceditos no token")
print (result.get("scope", "N/A"))

url = 'https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq false&$select=displayName,userPrincipalName,accountEnabled,signInActivity &$top=999'

headers = {'Authorization': 'Bearer {}'.format(result['access_token'])}
response = requests.get(url, headers=headers)


# Testar chamada simples à API
url = 'https://graph.microsoft.com/v1.0/users?$top=1'
headers = {
        'Authorization': 'Bearer {}'.format(result['access_token'])}
if response.status_code !=200:
    print ("Fail at API call: {}".format(response.status_code, response.text))
    exit(1)

print ("users diabled for more than {} days".format(inactive_days))    

#filter by inactivity

data = response.json
users = data.get('value',[])
today = datetime.timedelta.now (datetime.UTC)
limit = datetime.timedelta(days=inactive_days)

for user in users:
     display_name - user,get ("displayName", "No Name")
     upn = user.get ("userPrincipalName", "No UPN")
     last_signin = user.get ("singInActivity", {}).get("LastSingInDateTime")

     if last_signin:
          data_login = datetime.datetime.fromisoformat(last_signin.replace("Z", "+00:00"))
          if today - data_login > limit:
               print ("Ultimo login em {}".format(display_name, upn))
     else:
        print("no logon".format(display_name,upn))
        
# to be continued