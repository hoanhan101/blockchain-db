#!/usr/bin/env python3

"""
	test_blockchain.py - Test Local Blockchain
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

from blockchain import Blockchain
from pprint import pprint

if __name__ == '__main__':

    """

    blockchain = Blockchain()
    previous_block = blockchain.last_block

    # How to make index immutable
    previous_block['index'] = 10
    previous_block['timestamp'] = 10
    previous_block['proof'] = 10

    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    print('Previous block: {0}'.format(previous_block))
    print('Previous proof: {0}'.format(previous_proof))
    print('Previous hash: {0}'.format(previous_hash))

    # Find the proof of work of the last block
    next_proof = blockchain.find_proof_of_work(previous_proof)

    # Use that to generate next block
    blockchain.generate_next_block(next_proof)
    last_block = blockchain.last_block
    print('Last block: {0}'.format(last_block))
    
    
    """

    # init a blockchain
    blockchain = Blockchain()

    print('\n START BLOCKCHAIN \n')
    pprint(blockchain[0])

    # fixed numbers of block to generate
    # NUMBER_OF_NODES = 10
    #
    # for i in range(NUMBER_OF_NODES):
    #     last_block = blockchain.last_block
    #     last_proof = last_block['proof']
    #     last_hash = blockchain.hash(last_block)
    #
    #     next_proof = blockchain.find_proof_of_work(last_proof)
    #
    #     blockchain.generate_next_block(next_proof)
    #
    #
    # print('\n AFTER GENERATING {0} BLOCKS \n'.format(NUMBER_OF_NODES))
    # pprint(blockchain.chain)
