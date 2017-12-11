#!/usr/bin/env python3

"""
	new_blockchain_db.py - BlockchainDB
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/3/2017
"""

import hashlib
import json
from time import time, ctime
from pymongo import MongoClient
from src.constant import *

class BlockchainDB(object):
    def __init__(self, IP=mongodb_IP, port=mongodb_port):
        """
        Initialize a chain of block, aka BlockChain.
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

        self.elapsed_time = 0
        self.hash_power = 0

        # Create a genesis block, only runs once time when creating a database
        # self.generate_genesis_block()

    def generate_genesis_block(self):
        """
        Generate a genesis block with None previous hash and 0 nonce.
        :return: None
        """
        self.generate_next_block(previous_hash=None, nonce=0)

    def generate_next_block(self, nonce, previous_hash=None):
        """
        Generate a new block in the BlockChain.
        :param nonce: The nonce which is calculated by Proof of Work.
        :param previous_hash: Hash of previous block
        :return: New block
        """
        # Define a block
        block = {
            "previous_block": self.get_length(),
            'height': self.get_length() + 1,
            'timestamp': ctime(time()),
            'transactions': self.transactions,
            "merkle_root": self.find_merkle_root(self.get_transaction_ids()),
            'number_of_transaction': len(self.transactions),
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash_json_object(self.get_last_block()),
            'block_reward': self.calculate_block_reward(),
            'difficulty_bits': self.calculate_difficulty_bits(),
            'difficulty': self.calculate_difficulty(),
            'elapsed_time': "%.4f seconds" % self.elapsed_time,
            'hash_power': "%ld hashes per second" % self.hash_power
        }

        # Reset the current list of transactions
        self.transactions = []

        # Insert to the database
        self.blocks.insert_one(block)

        print('Block #{0} added to the chain'.format(block['height']))

        return block

    def add_transaction(self, sender, recipient, amount):
        """
        Add a new transaction to the block.
        :param sender: Address of Sender
        :param recipient: Address of Recipient
        :param amount: Amount of coin
        :return: Index of the next mined block
        """
        # Prepare the transaction information
        transaction_info = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }

        # Get the transaction id by hashing its content
        transaction_id = self.hash_json_object(transaction_info)

        # Append to the list of transactions
        self.transactions.append({
            'transaction_id': transaction_id,
            'transaction_info': transaction_info
        })

    def find_merkle_root(self, transaction_ids):
        """
        Find a merle root for a given list of transaction.
        :param transaction_ids: List of transaction
        :return: Hash value
        """
        # Exception: if there is no transaction ids, return None
        if len(transaction_ids) == 0:
            return None

        # Base case: if there is only 1 transaction, return the hash of that transaction
        if len(transaction_ids) == 1:
            return transaction_ids[0]

        # Otherwise, create a new hash list
        new_list = []

        # Go through list of transaction_ids, hash pairs of items together and add them to the new list
        for i in range(0, len(transaction_ids) - 1, 2):
            new_list.append(self.hash_string_pair(transaction_ids[i], transaction_ids[i + 1]))

        # If the length of the transaction_ids is odd, which means there is only one left over,
        # hash the last transaction with itself.
        if len(transaction_ids) % 2 == 1:
            new_list.append(self.hash_string_pair(transaction_ids[-1], transaction_ids[-1]))

        # Recursively do it all over again until there is one left
        return self.find_merkle_root(new_list)

    def mine_for_next_block(self):
        """
        Find the nonce for the next block and add it to the chain.
        :return: None
        """
        # Assume the address of sender and recipient is fixed when mining a block
        reward = {
            'sender': '00000000000000000000x0',
            'recipient': '00000000000000000000x1',
            'amount': self.calculate_block_reward()
        }

        last_block = self.get_last_block()
        last_difficulty_bits = last_block['difficulty_bits']

        start_time = time()

        # Find nonce for the next block, given the last block and level of difficulty
        next_nonce = self.calculate_nonce(last_block, last_difficulty_bits)

        # Checkpoint how long it took to find a result
        end_time = time()
        self.elapsed_time = end_time - start_time

        # Estimate the hashes per second
        if self.elapsed_time > 0:
            self.hash_power = float(int(next_nonce) / self.elapsed_time)

        # Reward miner
        self.add_transaction(reward['sender'], reward['recipient'], reward['amount'])

        # Add that block to the chain
        self.generate_next_block(next_nonce)

    def calculate_nonce(self, last_block, number_of_bits):
        """
        Calculate nonce using Proof Of Work algorithm.
        Based on the implementation at http://chimera.labs.oreilly.com/books/1234000001802/ch08.html#_proof_of_work_algorithm
        :param last_block: Last block
        :param number_of_bits: Number of difficulty bits
        :return: Int if succeed, None if fail
        """
        # Calculate the difficulty target
        target = 2 ** (256 - number_of_bits)

        # Constantly increase nonce by 1 and guess the right nonce
        for nonce in range(max_nonce):
            string = (str(last_block) + str(nonce)).encode()
            hash_result = hashlib.sha256(string).hexdigest()

            # Check if the hash result is below the target
            if int(hash_result, 16) < target:
                return nonce

        return None

    def hash_json_object(self, json_object):
        """
        Create a SHA-256 hash of a JSON object.
        :param json_object: JSON object
        :return: String as hash value
        """
        # Make sure data is sorted, otherwise would have inconsistent hashes
        json_string = json.dumps(json_object, sort_keys=True).encode()
        hash_string = hashlib.sha256(json_string).hexdigest()
        return hash_string

    def hash_string_pair(self, string_1, string_2):
        """
        Return a hash value for a given pair of string.
        :param string_1: String
        :param string_2: String
        :return: String as hash value
        """
        # Concat 2 string and encode them
        temp_string = (string_1 + string_2).encode()

        # Get the hash value
        hash_string = hashlib.sha256(temp_string).hexdigest()
        return hash_string

    def calculate_block_reward(self):
        """
        Calculate block reward for the next mined block.
        Cut reward by half for every n blocks, until it eventually reduces to 0.
        :return: Int
        """
        last_block = self.get_last_block()

        # If we don't have any block yet, meaning that we are creating the genesis block
        # set the block reward to 50
        if last_block == None:
            return init_reward

        # Otherwise get the last block reward and its height
        current_reward = last_block['block_reward']
        current_height = last_block['height']

        # If the current block reward is larger than 1 and its height is divisible by n
        # then divide the block reward in half.
        if current_reward > 1 and current_height % block_reward_rate == 0:
            current_reward /= 2
            return current_reward
        # If it goes below 1, then no more reward is given!
        elif current_reward < 1:
            return 0
        else:
            return current_reward

    def calculate_difficulty_bits(self):
        """
        Calculate the difficulty bits for the next mined block.
        For every n blocks, increase the difficulty bits by 1.
        :return: Int
        """
        last_block = self.get_last_block()

        # If we don't have any block yet, meaning that we are creating the genesis block
        # set the difficulty bits to 0
        if last_block == None:
            return 0

        # Otherwise, calculate the difficulty base on difficulty bits
        current_difficulty_bits = last_block['difficulty_bits']
        current_height = last_block['height']

        # If the current height is divisible by 10,
        # increase the difficulty exponentially by power of 2
        if current_height % difficulty_bits_block_rate == 0:
            current_difficulty_bits += 1
            return current_difficulty_bits
        else:
            return current_difficulty_bits

    def calculate_difficulty(self):
        """
        Calculate the difficulty for the next mined block.
        For every n blocks, since the difficulty bits is increased by 1,
        the difficulty will increase exponentially by the number of 2.
        """
        last_block = self.get_last_block()

        # If we don't have any block yet, meaning that we are creating the genesis block
        # set the difficulty to 1
        if last_block == None:
            return 1

        # Otherwise, calculate the difficulty base on difficulty bits
        current_difficulty_bits = last_block['difficulty_bits']
        current_difficulty = last_block['difficulty']
        current_height = last_block['height']

        # If the current height is divisible by 10,
        # increase the difficulty exponentially by power of 2
        if current_height % difficulty_block_rate == 0:
            current_difficulty_bits += 1
            difficulty = 2 ** current_difficulty_bits
            return difficulty
        else:
            return current_difficulty

    def get_length(self):
        """
        Get the length of BlockChain.
        :return: Int
        """
        return self.blocks.count()

    def get_last_n_blocks(self, number):
        """
        Get last n given number of blocks.
        :param number: Number of blocks
        :return: Dictionary as a list of blocks
        """
        return self.blocks.find({}, {'_id': 0}).sort([('height', -1)]).limit(number)

    def get_last_block(self):
        """
        Get last block of the chain.
        :return: Dictionary
        """
        return self.blocks.find_one({'height': self.get_length()}, {'_id': 0})

    def get_genesis_block(self):
        """
        Get first block of the chain.
        :return: Dictionary
        """
        return self.blocks.find_one({'height': 1}, {'_id': 0})

    def get_block(self, height):
        """
        Get a block given height number.
        :return: Dictionary
        """
        return self.blocks.find_one({'height': height}, {'_id': 0})

    def get_all_blocks(self):
        all_blocks = self.blocks.find({}, {'_id': 0})
        return all_blocks

    def get_transaction_ids(self):
        """
        Get a list of transaction ids.
        :return: List of transaction ids.
        """
        transaction_ids = []
        for transaction in self.transactions:
            transaction_id = transaction['transaction_id']
            transaction_ids.append(transaction_id)
        return transaction_ids