import os
import math
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from synapse import CerberusSynapse

# The 7.8 threshold is the industry standard for identifying high-entropy noise
THRESHOLD = 7.8

class CerberusAgent(FileSystemEventHandler):
    def __init__(self):
        print("[*] Cerberus Edge Agent v2.0 Initializing...")
        self.synapse = CerberusSynapse()

    def on_modified(self, event):
        if not event.is_directory:
            self.analyze_file(event.src_path)

    def calculate_entropy(self, data):
        if not data: return 0
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
                    print(f"\n[!] ALERT: High Entropy [{entropy:.4f}] in {os.path.basename(file_path)}")
                    # DISPATCH TO CLOUD: Sending the first 64 bytes as a hex dump for the dashboard
                    self.synapse.emit_alert(file_path, entropy, data[:64].hex())
                else:
                    print(f"[*] Monitoring Integrity... [{entropy:.2f}]", end='\r')
        except Exception:
            pass

if __name__ == "__main__":
    path = "./vault"
    event_handler = CerberusAgent()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    
    print("--- CERBERUS v2.0: CLOUD_UPLINK_PROTOCOL ---")
    print("Status: EDGE_NODE_ACTIVE")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
