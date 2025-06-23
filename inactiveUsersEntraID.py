import os
from dotenv import load_dotenv
import requests
from msal import ConfidentialClientApplication
import sys

# Carregar variáveis do .env

load_dotenv(".env") #chaves de acesso
load_dotenv("parametros.env") #paramtros adicionais

#leitura das chaves de acesso
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

url = 'https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq false&$select=displayName,userPrincipalName,accountEnabled,signInActivity&$top=999'

headers = {'Autorization': 'Bearer {}'.format(result['access-token'])}
response = requests.get(url, headers=headers)


# Testar chamada simples à API
url = 'https://graph.microsoft.com/v1.0/users?$top=1'
headers = {
        'Authorization': 'Bearer {}'.format(result['access_token'])}
if response.status_code !=200:
    print ("Fail at API call: {}".format(response.status_code, response.text)).exit(1)

print ("users diabled for more than {} days".format(inactive_days))    

#filter by inactivity

data = response.json
users = data.get('value',[])


 #response = requests.get(url, headers=headers)

#if response.status_code == 200:
#        print("API Call succeed!")
#else:
#        print("Fail at API call: {} - {}".format(response.status_code, response.text))

#else:
 #   print("Authentication failed!")
  #  print("Details:")
   # for k, v in result.items():
    #    print("{}: {}".format(k, v))