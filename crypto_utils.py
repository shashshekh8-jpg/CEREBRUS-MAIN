import random
import math

class CerberusCrypto:
    @staticmethod
    def generate_rsa_keys(p=61, q=53):
        """Generates a simple RSA key pair for authorized vault operations."""
        n = p * q
        phi = (p-1) * (q-1)
        
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        e = random.randrange(1, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(1, phi)
            
        def multiplicative_inverse(e, phi):
            d, x1, x2, y1, y2, temp_phi = 0, 0, 1, 1, 0, phi
            while e > 0:
                temp1, temp2 = temp_phi // e, temp_phi % e
                temp_phi, e = e, temp2
                x, y = x1 - temp1 * x2, y1 - temp1 * y2
                x1, x2, y1, y2 = x2, x, y2, y
            return y1 if temp_phi == 1 else None
            
        d = multiplicative_inverse(e, phi)
        return ((e, n), (d, n))

    @staticmethod
    def sign_data(data):
        """Simulates an authorized signature header for Cerberus."""
        return b"CERBERUS_SIG::" + data
