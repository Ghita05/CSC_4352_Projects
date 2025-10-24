import random

def create_hash_functions(num_hashes, p=2**31 - 1):
    funcs = []
    for _ in range(num_hashes):
        a = random.randint(1, p - 1)
        b = random.randint(0, p - 1)
        funcs.append((a, b, p))
    return funcs

def compute_minhash_signature(feature_set, hash_funcs):
    signature = []
    for a, b, p in hash_funcs:
        min_val = min(((a * x + b) % p) for x in feature_set)
        signature.append(min_val)
    return signature

def hash_to_set(phash_int, n_bits=64):
    return {i for i in range(n_bits) if (phash_int >> i) & 1}
