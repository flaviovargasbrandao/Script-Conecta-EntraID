import os
from dotenv import load_dotenv
import requests
from msal import ConfidentialClientApplication

# Carregar variáveis do .env
load_dotenv('.env.decrypted')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')

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

if "access_token" in result:
    print("Connection with EntraID established")

    # Testar chamada simples à API
    url = 'https://graph.microsoft.com/v1.0/users?$top=1'
    headers = {
        'Authorization': 'Bearer {}'.format(result['access_token'])
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API Call succeed")
    else:
        print("Fail on the API call: {} - {}".format(response.status_code, response.text))

else:
    print("Authentication Failed")
    print("Details:")
    for k, v in result.items():
        print("{}: {}".format(k, v))