#!/usr/bin/env python3

"""
	blockchain.py - Blockchain
	Inspired by Daniel van Flymen's blockchain repo at: https://github.com/dvf/blockchain
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

import hashlib
import json
from time import time, ctime
from pymongo import MongoClient

class BlockchainDB(object):
    def __init__(self, IP='localhost', port=27017):
        """
        Initialize a chain of block, Blockchain.
        :param IP: IP
        :param port: Port
        """
        # Setup MongoClient
        self.client = MongoClient(IP, port)

        # Connect to blockchain database
        self.db = self.client.blockchain

        # Drop
        # self.db.blocks.drop()

        # Use the blocks collection
        self.blocks = self.db.blocks

        # Save all the transactions in memory,
        # only write to database when miner successfully mine a new block
        self.transactions = []

        self.nodes = set()

        # Create a genesis block, only runs once time when creating a database
        # self.generate_genesis_block()

    def get_length(self):
        """
        Get the length of Blockchain.
        :return: Int
        """
        return self.blocks.count()

    def get_last_block(self):
        """
        Get last block of the chain.
        :return: Dictionary
        """
        return self.blocks.find_one({'index': self.get_length()}, {'_id': 0})

    def get_genesis_block(self):
        """
        Get first block of the chain.
        :return: Dictionary
        """
        return self.blocks.find_one({'index': 1}, {'_id': 0})

    def get_blockchain(self):
        blockchain = self.blocks.find({})
        return blockchain

    def generate_genesis_block(self):
        """
        Generate a genesis block with hard coded previous hash and proof
        :return: None
        """
        self.generate_next_block(previous_hash=None, proof=0)

    def generate_next_block(self, proof, previous_hash=None):
        """
        Generate a new block in the blockchain.
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous block
        :return: New block
        """
        # Define a block
        block = {
            'index': self.get_length() + 1,
            'timestamp': ctime(time()),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.get_last_block()),
        }

        # Reset the current list of transactions
        self.transactions = []

        # Insert to the database
        self.blocks.insert_one(block)

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

    def mine_for_next_block(self):
        """
        Find the proof of work for the next block and add it to the chain.
        :return:
        """
        # Assume the address of sender and recipient is fixed when mining a block
        reward = {
            'sender': '7edcae61fc564b4d92b78384db5479f2',
            'recipient': 'a42655958f9a4b3a986791b41450a034',
            'amount': 1
        }

        last_block = self.get_last_block()
        last_proof = last_block['proof']

        # Find the proof of work for the next block
        next_proof = self.find_proof_of_work(last_proof)

        # Reward miner
        self.add_transaction(reward['sender'], reward['recipient'], reward['amount'])

        # Add that block to the chain
        self.generate_next_block(next_proof)

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
        print(guess_hash)
        return guess_hash[:4] == '0000'

    @staticmethod
    def hash(json_object):
        """
        Create a SHA-256 hash of a JSON object.
        :param block: Block
        :return: Hash string
        """
        # Make sure data is sorted, otherwise would have inconsistent hashes
        json_string = json.dumps(json_object, sort_keys=True).encode()
        hash_string = hashlib.sha256(json_string).hexdigest()
        return hash_string