from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate ECC private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Get public key from the private key
public_key = private_key.public_key()

# Export private key in PEM format
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Export public key in PEM format
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Export public key in base64-encoded DER format (for load_der_public_key)
public_key_der = public_key.public_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
public_key_b64 = base64.b64encode(public_key_der).decode('utf-8')

# Print results
print("=== ECC PRIVATE KEY (PEM) ===")
print(private_key_pem.decode())

print("=== ECC PUBLIC KEY (PEM) ===")
print(public_key_pem.decode())

print("=== ECC PUBLIC KEY (Base64 DER) ===")
print(public_key_b64)