import requests
import json
import time
import os

class CerberusSynapse:
    def __init__(self):
        # Your Vercel API endpoint
        self.api_url = "https://cerberus-rust.vercel.app/api/incident"
        # Secret token for authentication
        self.secret = "CERBERUS_LOCAL_AGENT_SECRET_2026"

    def emit_alert(self, file_path, entropy, hex_dump):
        payload = {
            "machineId": "EDGE_NODE_BOM1",
            "fileName": os.path.basename(file_path),
            "entropyScore": entropy,
            "hexDump": hex_dump,
            "status": "DETECTED",
            "timestamp": int(time.time() * 1000)
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-agent-secret": self.secret
        }

        try:
            print("[^] Uplink: Sending telemetry to Cerberus Cloud...")
            response = requests.post(self.api_url, json=payload, headers=headers)
            if response.status_code == 200:
                print("[+] Uplink: Signal Received and Broadcasted.")
            else:
                print(f"[!] Uplink Failure: {response.status_code}")
        except Exception as e:
            print(f"[!] Critical Uplink Error: {e}")
