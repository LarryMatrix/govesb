import base64
import json
import requests
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from crypto.Cipher import AES
from crypto.Random import get_random_bytes
# from typing import Optional, Dict
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes




class GovEsbHelper:
    def __init__(self):
        self.client_private_key = '''-----BEGIN PRIVATE KEY-----
MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg0p9NBRwrzUd7QDy9/VJ1
hll1s/G/A1L53H9qi80PpgGhRANCAATBkC9S4xxAToW6mUxE2WhujOQFOfk9ZBDS
5aEOmyE3uuzLCbFK1l1MzepsohczMIHfRxxO48WYpBI+/YRDKB/9
-----END PRIVATE KEY-----'''
        self.encryption_private_key = '''-----BEGIN PRIVATE KEY-----
MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQg0p9NBRwrzUd7QDy9/VJ1
hll1s/G/A1L53H9qi80PpgGhRANCAATBkC9S4xxAToW6mUxE2WhujOQFOfk9ZBDS
5aEOmyE3uuzLCbFK1l1MzepsohczMIHfRxxO48WYpBI+/YRDKB/9
-----END PRIVATE KEY-----'''
        self.esb_public_key = '''-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEwZAvUuMcQE6FuplMRNlobozkBTn5PWQQ
0uWhDpshN7rsywmxStZdTM3qbKIXMzCB30ccTuPFmKQSPv2EQygf/Q==
-----END PUBLIC KEY-----'''
        self.client_id = '872ce6f8-fc51-11ec-9b90-b92089927798'
        self.client_secret = 'yQew0P4oxZiX517ZsgT0OL9QWrvoEDNH'
        self.esb_token_url = 'https://esbdemo.gov.go.tz/gw/govesb-uaa/oauth/token'
        self.esb_engine_url = 'https://esbdemo.gov.go.tz/engine/esb'
        self.nida_user_id = '123456'
        self.api_code = '12345'
        self.request_body = None
        self.format = 'json'
        self.access_token = None

    def get_access_token(self):
        auth = f"{self.client_id}:{self.client_secret}"
        encoded_auth = base64.b64encode(auth.encode()).decode()
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(self.esb_token_url, data=data, headers=headers)
        token_response = response.json()
        if response.status_code == 200 and "access_token" in token_response:
            self.access_token = token_response["access_token"]
            return token_response
        raise Exception("Could not get access token from ESB")

    def sign_payload_ecc(self, payload: str) -> str:
        key = serialization.load_der_private_key(
            base64.b64decode(self.client_private_key),
            password=None,
            backend=default_backend()
        )
        signature = key.sign(payload.encode(), ec.ECDSA(hashes.SHA256()))
        return base64.b64encode(signature).decode()

    def verify_payload_ecc(self, data: str, signature: str) -> bool:
        pub_key = serialization.load_der_public_key(
            base64.b64decode(self.esb_public_key),
            backend=default_backend()
        )
        try:
            pub_key.verify(
                base64.b64decode(signature),
                data.encode(),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False

    def encrypt_ecies(self, plain_data: str) -> str:
        pub_key = serialization.load_der_public_key(
            base64.b64decode(self.esb_public_key),
            backend=default_backend()
        )
        ephemeral_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        shared_key = ephemeral_key.exchange(ec.ECDH(), pub_key)
        aes_key = shared_key[:16]

        cipher = AES.new(aes_key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plain_data.encode())

        return json.dumps({
            "encryptedKey": base64.b64encode(
                ephemeral_key.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
            ).decode(),
            "encryptedData": base64.b64encode(cipher.nonce + ciphertext + tag).decode()
        })

    def decrypt_ecies(self, encrypted_aes_key: str, encrypted_data: str) -> str:
        priv_key = serialization.load_der_private_key(
            base64.b64decode(self.encryption_private_key),
            password=None,
            backend=default_backend()
        )
        aes_key = priv_key.private_numbers().private_value.to_bytes(32, 'big')[:16]
        raw = base64.b64decode(encrypted_data)
        nonce, ciphertext, tag = raw[:16], raw[16:-16], raw[-16:]
        cipher = AES.new(aes_key, AES.MODE_EAX, nonce)
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode()

    def convert_pem(self, pem_string: str, is_private: bool = False) -> bytes:
        if is_private:
            return base64.b64decode(
                pem_string.replace("-----BEGIN EC PRIVATE KEY-----", "")
                .replace("-----END EC PRIVATE KEY-----", "")
                .replace("\n", "")
            )
        return base64.b64decode(
            pem_string.replace("-----BEGIN PUBLIC KEY-----", "")
            .replace("-----END PUBLIC KEY-----", "")
            .replace("\n", "")
        )
