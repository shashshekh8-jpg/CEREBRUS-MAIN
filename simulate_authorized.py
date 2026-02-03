# Utility to simulate an authorized Cerberus write
import os
from crypto_utils import CerberusCrypto

crypto = CerberusCrypto()
data = b"Sensitive information encrypted by Cerberus."
signed_data = crypto.sign_data(os.urandom(1024)) # High entropy random data with signature

with open("./vault/authorized_test.db", "wb") as f:
    f.write(signed_data)
print("[+] Created authorized high-entropy file in ./vault/")
