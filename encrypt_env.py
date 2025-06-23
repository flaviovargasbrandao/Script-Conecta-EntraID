from cryptography.fernet import Fernet

#genearate a criptography key for env file
key = Fernet.generate_key()
print("Encryption Key: {}".format(key.decode()))

#initialize Fernet with the key
cipher = Fernet(key)

#read the .env file
with open('.env','rb') as file:
    env_data = file.read()

#encrypt the data
encrypted_data = cipher.encrypt(env_data)

#write the encrypted data to a new file
with open('.env.encrypted', 'wb') as file:
    file.write(encrypted_data)
print ("Encrypted .env file created as .env.encrypted")



