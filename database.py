#!/usr/bin/env python3

"""
	database.py - Test mongodb on top of blockchain
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

from blockchain import Blockchain

from pymongo import MongoClient
from pprint import pprint

if __name__ == '__main__':
    # Setup MongoClient
    client = MongoClient('localhost', 27017)

    # Connect to blockchain database
    db = client.blockchain

    # Use the blocks collection
    blocks = db.blocks

    """
    
    # Init Blockchain
    blockchain = Blockchain()
    previous_block = blockchain.last_block

    # Insert genesis block
    # blocks.insert_one(previous_block)

    # Generate next block and insert to blocks
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)

    # Find the proof of work of the last block
    next_proof = blockchain.find_proof_of_work(previous_proof)

    # Use that to generate next block
    blockchain.generate_next_block(next_proof)
    last_block = blockchain.last_block

    # Insert last block we just generated to the blocks
    blocks.insert_one(last_block)

    """


    # Print out all the blocks
    all_blocks = blocks.find({})
    for block in all_blocks:
        pprint(block)

    length = blocks.count()
    print(length)

    last_record = blocks.find_one({'index': length}, {'_id': 0})
    pprint(last_record)

    blockchain = Blockchain()
    hash_last_record = blockchain.hash(last_record)
    print(hash_last_record)

    """
        TODO:
            - Instead of store blockchain in a list, which is in memory
            - Store in a local database
            - Retrieve, update, append into that.
            
            - Need to get first peer working first
            - Start add more peer
    """