# Importing the required libraries
import datetime # For each block's timestamp
import hashlib # For the blocks hashes
import json # To encode the blocks before hashing them
from flask import Flask, jsonify # For the web application itself

# 1 - Creating the Blockchain
# 1.1 - Building the Blockchain skeleton
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0') # Creating the genesis block of the Blockchain. "proof" is the nounce, the proof that the miner has worked its way to mine the block
