from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load the encrypted .env file
load_dotenv(".env")

# Check if the encryption key is set in the environment
key = os.getenv('ENCRYPTION_KEY')

if not key:
    print ("Encryption key not found")
    exit(1)

 #Initiate the Fernet cipher with the key   
cipher = Fernet(key)

#read the cypher key from the .env file

with open ('.env.encrypted', 'rb') as file:
    encrypted_data = file.read()

#decrypt the data
decrypted_data = cipher.decrypt(encrypted_data)

#Save the decrypted data to a new file
with open('.env.decrypted', 'wb') as file:
    file.write(decrypted_data)
print ("Decrypted .env file created")
