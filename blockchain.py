"""
Created on Fri Apr  7 12:11:51 2023

@author: zelimirmaletic
"""

import datetime
import hashlib
import json
import config
import RSA_Class

counter = 1
class Blockchain:


    def __init__(self):
        # Initialize a chain which will contain blocks
        self.chain = []  # a simple list containing blovks
        # Create a genesis block - the first block
        # Previous hash is 0 because this is a genesis block!
        self.create_block(proof=1, previous_hash='0', data=None)

    def create_block(self, proof, previous_hash, data):
        # Define block as a dictionary
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 # Here we can add any additional data...
                 }

        encrypted = RSA_Class.encrypt(data)

        # Add field2 to the existing data
        block["data"] = encrypted

        # Convert the updated data to JSON
        # block_json = json.dumps(block, indent=4)

        self.create_json_file(block)
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1  # nonce value
        check_proof = False
        while check_proof is False:
            # Problem to be solved (this makes the minig hard)
            # operation has to be non-symetrical!!!
            hash_operation = hashlib.sha256(
                str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(previous_proof, new_proof)).encode()).hexdigest()
            # Check if first 4 characters are zeros
            if hash_operation[:len(config.LEADING_ZEROS)] == config.LEADING_ZEROS:
                check_proof = True
            else:
                new_proof += 1
        # Check proof is now true
        return new_proof

    def hash_of_block(self, block):
        # Convert a dictionary to string (JSON)
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # 1 Check the previous hash
            block = chain[block_index]
            if block['previous_hash'] != self.hash_of_block(previous_block):
                return False
            # 2 Check all proofs of work
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(config.BLOCKCHAIN_PROBLEM_OPERATION_LAMBDA(previous_proof, proof)).encode()).hexdigest()
            if hash_operation[:len(config.LEADING_ZEROS)] != config.LEADING_ZEROS:
                return False
            # Update variables
            previous_block = block
            block_index += 1
        return True

    def create_json_file(self,data):
        global counter
        file_name = f"book{counter}.json"
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
        counter += 1





















