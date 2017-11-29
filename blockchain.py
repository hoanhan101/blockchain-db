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

class Blockchain(object):
    def __init__(self):
        """
        Initialize a chain of block, Blockchain, with a list of transactions
        and a set of nodes.
        """
        self.chain = []
        self.transactions = []
        self.nodes = set()

        # Create a genesis block
        self.generate_next_block(previous_hash=1, proof=100)

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
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.transactions = []

        # Add to the blockchain
        self.chain.append(block)

        return block

    def add_transaction(self, sender, recipient, amount):
        """
        Add a new transaction to the block.
        :param sender: Address of Sender
        :param recipient: Address of Recipient
        :param amount: Amount of coin
        :return: Index of the next mined block
        """
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

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

    def verify_chain(self, chain):
        """
        Check if a given blockchain is valid by looping through each block
        and verifying its hash and proof.
        :param chain: A blockchain
        :return: True if valid, False if not
        """
        # Set the first block to last block variable
        last_block = chain[0]

        # Begin with index 1
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]

            # Check if the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check if the Proof of Work is correct
            if not self.verify_proof_of_work(last_block['proof'], block['proof']):
                return False

            # If passes, set the last block to the one we are visiting
            last_block = block

            # Increase the current index by 1
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Resolves conflicts by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """
        neighbours = self.nodes
        new_chain = None

        # Set our chain length to max length
        max_length = len(self.chain)

        # Loop through all our neighbouring nodes
        for node in neighbours:
            # Get its chain
            response = requests.get('http://{0}/chain'.format(node))

            if response.status_code == 200:
                chain = response.json()['chain']
                length = response.json()['length']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.verify_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

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

    @property
    def last_block(self):
        return self.chain[-1]