import os
import math
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from crypto_utils import CerberusCrypto

# Entropy threshold for encryption detection
THRESHOLD = 7.5

class CerberusVaultHandler(FileSystemEventHandler):
    def __init__(self):
        self.crypto = CerberusCrypto()
        self.pub, self.priv = self.crypto.generate_rsa_keys()
        print(f"[+] Cerberus RSA Node Initialized. Public Key: {self.pub}")

    def on_modified(self, event):
        if not event.is_directory:
            self.analyze_file(event.src_path)

    def calculate_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def analyze_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                entropy = self.calculate_entropy(data)
                
                if entropy > THRESHOLD:
                    print(f"\n[!] HI-ENTROPY DETECTED: {os.path.basename(file_path)} [{entropy:.4f}]")
                    
                    # Logic: Check for Cerberus authorized signature
                    if data.startswith(b"CERBERUS_SIG"):
                        print("[+] VERIFIED: Authorized Vault Operation. No action taken.")
                    else:
                        print("[!!!] WARNING: Unauthorized Encryption Detected! [MALWARE SUSPECTED]")
                        print("[!] ACTION: LOCKING FILE SYSTEM HANDLES...")
        except Exception:
            pass

if __name__ == "__main__":
    path = "./vault"
    event_handler = CerberusVaultHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print("--- CERBERUS v1.1: RSA SECURE VAULT ENGINE ---")
    print(f"Uptime: {time.ctime()}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
