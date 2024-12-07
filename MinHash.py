import numpy as np
from sympy import *

class MinHash:
    def __init__(self, max_val,num_hashes=100):
        """
        Constructor of the MinHash object.
        
        :param num_hashes: Number of hash functions to use(default= 100)
        :param max_val: Value based on which the property prime is computed
        """
        self.num_hashes = num_hashes
        self.prime = nextprime(max_val)
        # Generate random hash function coefficients
        self.coef = [
            (np.random.randint(1, self.prime), np.random.randint(0,self.prime)) 
            for _ in range(num_hashes)
        ]
    def hash_function(self, x, a, b,type):
        """
        Hash function: 
        Type 1:(a * x + b) % prime
        Type 2:(2*a * x + b) % prime
        Type 3:(3*a * x + b) % prime
        :param x: Value to hash
        :param a: Random coefficient
        :param b: Random bias
        :return: Computed hash value
        """
        if type==2:
            return (2*a * x +b) % self.prime
        elif type==3:
            return (3*a * x +b) % self.prime
        else:
            return (a * x +b) % self.prime


    def generate_signature(self, input_set,type=1):
        """Compute the MinHash signature for the given set.
        
        :param input_set: The input set of elements (integers)
        :return: A list of minhash values (signature)
        """
        signature = []
        for a, b in self.coef:
            min_hash = float('inf')
            for x in input_set:
                min_hash = min(min_hash, self.hash_function(x, a, b,type))
            signature.append(min_hash)
        return signature

    @staticmethod
    def signature_similarity(sig_a, sig_b):
        """Estimate the Jaccard similarity using MinHash signatures.
        
        :param sig_a: MinHash signature of set A
        :param sig_b: MinHash signature of set B
        :return: Similarity score
        """
        matches = sum(1 for a, b in zip(sig_a, sig_b) if a == b)
        return matches / len(sig_a)
        
    @staticmethod
    def jaccard_similarity(set_a, set_b):
        """Compute the Jaccard similarity between two sets.
        
        :param set_a: First set
        :param set_b: Second set
        :return: Jaccard similarity value
        """
        intersection = len(set_a&set_b)
        union = len(set_a | set_b)
        return intersection / union if union != 0 else 0.0
    