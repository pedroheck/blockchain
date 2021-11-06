# Importing the required libraries
import datetime  # For each block's timestamp
import hashlib  # For the blocks hashes
import json  # To encode the blocks before hashing them
from flask import Flask, jsonify  # For the web application itself

'''
------------------------------------------------- CREATING THE BLOCKCHAIN -----------------------------------------------------
'''


class Blockchain:
    def __init__(self):
        self.chain = []
        # Creating the genesis block of the Blockchain. "proof" is the nounce, the proof that the miner has worked its way to mine the block
        self.create_block(proof=1, previous_hash='0')

    # mine_block() -> proof -> create_block()
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.chain.append(block)  # Adding the block to the chain
        return block

    def get_previous_block(self):
        # Friendly reminder that, in Python, the shortpath array[-1] gets the last item on the array
        return self.chain[-1]

    def proof_of_work(self, block):
        # json.dumps converts a Python object into a json string
        encoded_block = json.dumps(block, sort_keys=True).encode()
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(encoded_block + str(new_proof).encode()).hexdigest()
            # If hash starts with this number of zeros
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return hash_operation, new_proof

    def is_chain_valid(self, chain):
        # Initializing the previous_block as the first block of the chain so it can be moved along the chain (block -> block -> block)
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # proof_of_work() returns hash_operation (att to hash_operation) and new_proof (att to _, for it is not used here)
            hash_operation, _ = self.proof_of_work(previous_block)
            # We calculate the previous block's hash and check if it equals to the current block's "previous_hash" attribute
            if block['previous_hash'] != hash_operation:
                return False  # The blockchain is not valid
            hash_operation, _ = self.proof_of_work(block)
            # If hash doesn't start with that number of zeros
            if hash_operation[:4] != '0000':
                return False  # The blockchain is not valid
            previous_block = block  # Moving along the chain
            block_index += 1
        return True  # If it passes all of those conditions, the chain is valid


'''
------------------------------------------------- CREATING THE WEB APP -----------------------------------------------------
'''
app = Flask(__name__)  # Creating an instance of the Flask class. The first argument is the name of the application's module or package, which is "__name__" in this case

# Creating an instance of out Blockchain. From now on, the blockchain actually exists
blockchain = Blockchain()

# Route for mining the block


@app.route('/mine', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    # proof_of_work() returns two values: previous_hash and proof, in this order
    previous_hash, proof = blockchain.proof_of_work(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Congratulations, you have mined the block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'hash': blockchain.proof_of_work(block)[0], # When a function returns more than one value, we can filter them with [index]
        'previous_hash': block['previous_hash']
    }
    # 200 is the HTTP status code for "OK", meaning there are no errors and the request was successfull
    return jsonify(response), 200


# Route for getting the full blockchain
@app.route('/get-chain', methods=['GET'])
def get_blockchain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Runs the server on port 5000
