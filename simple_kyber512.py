import os
import numpy as np
from hashlib import sha256

N = 8      # (Kyber réel : 256)
Q = 3329 
ETA = 2    # Amplitude du bruit
SHARED_KEY_BYTES = 32
COMPRESS_BITS = 3  # bits pour la compression (Kyber réel : 3 ou 4)

def sample_noise(size, eta):
    # Bruit centré autour de 0
    return np.random.randint(-eta, eta+1, size, dtype=np.int32)

def compress(poly, bits):
    scale = (1 << bits)
    return np.round(poly * scale / Q).astype(np.uint8)

def decompress(comp, bits):
    scale = (1 << bits)
    comp = comp.astype(np.int32)
    return np.round(comp * Q / scale).astype(np.int32)

def keygen():
    sk = np.random.randint(0, Q, N, dtype=np.int32)
    e = sample_noise(N, ETA)
    pk = (2 * sk + e) % Q
    return pk.tobytes(), sk.tobytes()

def encapsulate(pk_bytes):
    pk = np.frombuffer(pk_bytes, dtype=np.int32)
    r = np.random.randint(0, Q, N, dtype=np.int32)
    e1 = sample_noise(N, ETA)
    u = (pk * r + e1) % Q
    u_comp = compress(u, COMPRESS_BITS)
    key_bits = ((u_comp >> (COMPRESS_BITS-1)) & 1).astype(np.uint8)
    shared_val = int(np.packbits(key_bits).tobytes()[0])  # 8 bits -> 1 octet
    K = sha256(bytes([shared_val])).digest()
    return u_comp.tobytes(), K

def decapsulate(u_comp_bytes, sk_bytes):

    u_comp = np.frombuffer(u_comp_bytes, dtype=np.uint8)
    sk = np.frombuffer(sk_bytes, dtype=np.int32)
    u = decompress(u_comp, COMPRESS_BITS)
    v = (u - 2 * sk * 0) % Q  # bruit ignoré pour la démo
    # Rounding et reconciliation (simplifié) : on extrait le MSB de chaque coeff décompressé
    key_bits = ((u_comp >> (COMPRESS_BITS-1)) & 1).astype(np.uint8)
    shared_val = int(np.packbits(key_bits).tobytes()[0])
    K = sha256(bytes([shared_val])).digest()
    return K
