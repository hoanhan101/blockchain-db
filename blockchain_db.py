#!/usr/bin/env python3

"""
	blockchain.py - Blockchain
	Based on Daniel van Flymen's blockchain repo at: https://github.com/dvf/blockchain
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse
from pymongo import MongoClient
from pprint import pprint

class BlockchainDB(object):
    def __init__(self, IP='localhost', port=27017):
        """
        Initialize a chain of block, Blockchain, with a list of transactions
        and a set of nodes.
        """
        # Setup MongoClient
        self.client = MongoClient(IP, port)

        # Connect to blockchain database
        self.db = self.client.blockchain

        # Start a new blocks collection
        self.db.blocks.drop()

        # Use the blocks collection
        self.blocks = self.db.blocks

        # self.chain = []
        self.transactions = []
        self.nodes = set()

        # Create a genesis block
        self.generate_next_block(previous_hash=1, proof=100)

    def get_length(self):
        return self.blocks.count()

    def get_last_block(self):
        return self.blocks.find_one({'index': self.get_length()}, {'_id': 0})

    def print_all_block(self):
        all_blocks = self.blocks.find({})
        for block in all_blocks:
            pprint(block)

    def generate_next_block(self, proof, previous_hash=None):
        """
        Generate a new block in the blockchain.
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous block
        :return: New block
        """
        # Define proof as an integer for simple computation.
        if not isinstance(proof, int):
            return False

        # Define a block
        block = {
            'index': self.get_length() + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.get_last_block()),
        }

        # Reset the current list of transactions
        self.transactions = []

        # Add to the blockchain
        # self.chain.append(block)
        self.blocks.insert_one(block)

        return block

    def find_proof_of_work(self, last_proof):
        """
        Return a proof such that hash of last proof and proof contains leading 4 zeroes.
        :param last_proof: Last proof number
        :return: Proof number
        """
        # Let proof number start at 0
        proof = 0

        # Increase the proof by 1 until we find the right value
        while self.verify_proof_of_work(last_proof, proof) is False:
            proof += 1

        return proof

    def register_node(self, address):
        """
        Add a new node to a list of nodes.
        :param address: Address of node
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    @staticmethod
    def verify_proof_of_work(last_proof, proof):
        """
        Check if the guess hash has 4 zeros in the front.
        :param last_proof: Previous proof
        :param proof: Current proof
        :return: True if correct, False if not.
        """
        guess = '{0}{1}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block.
        :param block: Block
        :return: Hash string
        """
        # Make sure data is sorted, otherwise would have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

if __name__ == '__main__':
    blockchain_db = BlockchainDB()
    print('\n Start BlockchainDB \n')
    blockchain_db.print_all_block()

    last_block = blockchain_db.get_last_block()
    last_proof = last_block['proof']

    next_proof = blockchain_db.find_proof_of_work(last_proof)
    blockchain_db.generate_next_block(next_proof)

    print('\n Finish adding to the blockchain \n')
    blockchain_db.print_all_block()