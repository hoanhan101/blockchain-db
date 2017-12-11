#!/usr/bin/env python3

"""
	blockchain_db_test.py - BlockchainDB Test
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""

from pprint import pprint
from random import randint
from uuid import uuid4

from temp.blockchain_db import BlockchainDB

if __name__ == '__main__':
    blockchain_db = BlockchainDB()
    # pprint(blockchain_db.get_genesis_block())
    # print('\n *** Start BlockchainDB *** \n')
    # for block in blockchain_db.get_blockchain():
    #     pprint(block)

    # print('\n *** Finish adding transaction. *** \n')
    # blockchain_db.add_transaction(sender='Vitalik Buterin', recipient='Hoanh An', amount=1)
    # blockchain_db.add_transaction(sender='Edward Snowden', recipient='Hoanh An', amount=2)
    # blockchain_db.add_transaction(sender='John McAfee', recipient='Hoanh An', amount=3)
    # blockchain_db.add_transaction(sender='Andreas Antonopoulos', recipient='Hoanh An', amount=4)
    # blockchain_db.add_transaction(sender='Joseph Lubin', recipient='Hoanh An', amount=5)
    # blockchain_db.add_transaction(sender='Gavin Andresen', recipient='Hoanh An', amount=6)
    # blockchain_db.add_transaction(sender='Roger Ver', recipient='Hoanh An', amount=7)
    # blockchain_db.add_transaction(sender='Nick Szabo', recipient='Hoanh An', amount=8)

    number_of_transactions = 10
    for i in range(number_of_transactions):
        blockchain_db.add_transaction(sender=(str(uuid4()).replace('-', '')), recipient=(str(uuid4()).replace('-', '')), amount=randint(1, 10))

    # Mine for next block
    # blockchain_db.mine_for_next_block()
    # blockchain_db.mine_for_next_block()
    # blockchain_db.mine_for_next_block()
    blockchain_db.mine_for_next_block()

    # print('\n *** Finish mining. Here is the current Blockchain *** \n')
    # for block in blockchain_db.get_blockchain():
    #     pprint(block)

    pprint(blockchain_db.get_last_block())


    # sample_block = {
    #       "height": 371623, # blochchain.get_height() -> return the db.collection.count()
    #       "merkleroot": "01a5f8b432e06c11a32b3f30e6cc9a12da207b9237fddf77850801275cf4fe01",
    #       "tx": ["ee6bc0e5f95a4ccd0f00784eab850ff8593f9045de96c6656df41c8f9f9c0888",
    #              "29c59ec39fc19afd84d928272b3290bbe54558f7b51f75feb858b005dea49c10"],
    #                 # save as an array in memory, append when need
    #       "time": 1440604813,   # unix time
    #       "nonce": 3431621579,  # counter start from 0, increase until find the proof
    #       "difficulty": 54256630327.88996,  # this is the proof?
    #       "previousblockhash": "0000000000000000027d0985fef71cbc05a5ee5cdbdc4c6baf2307e6c5db8591",
    #       "hash": "0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a",
    #       "nextblockhash": "000000000000000013677449d7375ed22f9c66a94940328081412179795a1ac5",
    #       "reward": 25,
    #       }
    # pprint(sample_block)