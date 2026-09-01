from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)
f = Fernet(key)
secret_message = "Hello World".encode()
cipher_text = f.encrypt(secret_message)
print(f"Encrypted Token: {cipher_text.decode()}")

decrypted_text = f.decrypt(cipher_text)
original_message = decrypted_text.decode()

print(f"Decrypted Message : {original_message}")





