from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import json
import RSA_Class
import blockchain

app = Flask(__name__)

# Create a Blockchain
blockchain = blockchain.Blockchain()


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/add', methods=['POST'])
def process_data():
    # Retrieve the JSON data from the request
    data = request.get_json()

    # Process the data (e.g., perform calculations, transformations, etc.)
    result = process(data)

    # Print the result
    print(result)

    # Get the previous proof
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    # Get previous hash
    previous_hash = blockchain.hash_of_block(previous_block)
    # Add new block to the blockchain
    block = blockchain.create_block(proof, previous_hash, data)
    # Generate a response as a dictionary
    response = {'message': 'Congratulations! You have added data!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'data': block['data']

                }
    return jsonify(response), 200

# Getting the full Blockchain


@app.route('/get-chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    return jsonify(response), 200

# Example function to process the data
def process(data):
    # Perform some processing on the data
    # Replace this with your own processing logic
    processed_data = data

    return processed_data






# Define the existing JSON as a dictionary
existing_data = {
    "field1": "value1"
}

# Create the field2 dictionary
field2 = {
    "attribute1": "attribute_value1",
    "attribute2": "attribute_value2"
}

encrypted = RSA_Class.encrypt(field2)

# Add field2 to the existing data
existing_data["field2"] = encrypted

# Convert the updated data to JSON
updated_json = json.dumps(existing_data, indent=4)



# Decrypt the field2 field as a JSON string
decrypted_field2_json = RSA_Class.decrypt_as_json(existing_data["field2"])

# Update the decrypted field2 in the data
decrypted_data = existing_data.copy()
decrypted_data["field2"] = json.loads(decrypted_field2_json)

# Convert the decrypted data to JSON
decrypted_json = json.dumps(decrypted_data, indent=4)




