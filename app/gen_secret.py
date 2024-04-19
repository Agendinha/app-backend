import secrets

# Gerar uma chave secreta aleatória com 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

print("Chave secreta gerada com sucesso:")
print(secret_key)