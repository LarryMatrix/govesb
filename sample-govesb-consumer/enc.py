from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# 1. Generate ECC private keys for both sender and receiver
sender_private_key = ec.generate_private_key(ec.SECP256R1())
receiver_private_key = ec.generate_private_key(ec.SECP256R1())

sender_public_key = sender_private_key.public_key()
receiver_public_key = receiver_private_key.public_key()

# 2. Derive shared secret using ECDH
shared_key_sender = sender_private_key.exchange(ec.ECDH(), receiver_public_key)
shared_key_receiver = receiver_private_key.exchange(ec.ECDH(), sender_public_key)

# 3. Derive symmetric AES key from shared secret
def derive_aes_key(shared_secret: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ecdh-aes-key',
    ).derive(shared_secret)

aes_key_sender = derive_aes_key(shared_key_sender)
aes_key_receiver = derive_aes_key(shared_key_receiver)

assert aes_key_sender == aes_key_receiver  # Should be the same

# 4. Encrypt a message using AES-GCM
def encrypt_message(key: bytes, plaintext: str) -> tuple:
    iv = os.urandom(12)  # 96-bit nonce for GCM
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv)
    ).encryptor()

    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return iv, ciphertext, encryptor.tag

# 5. Decrypt the message
def decrypt_message(key: bytes, iv: bytes, ciphertext: bytes, tag: bytes) -> str:
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag)
    ).decryptor()

    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

# Test it
message = "Hello from ECC + AES!"
iv, ciphertext, tag = encrypt_message(aes_key_sender, message)
print('ciphertext', ciphertext)
decrypted_message = decrypt_message(aes_key_receiver, iv, ciphertext, tag)

print("Original:", message)
print("Decrypted:", decrypted_message)