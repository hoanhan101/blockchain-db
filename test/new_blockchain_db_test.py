#!/usr/bin/env python3

"""
	new_blockchain_db_test.py - BlockchainDB Test
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""

from src.new_blockchain_db import BlockchainDB
from pprint import pprint
from uuid import uuid4
from random import randint

if __name__ == '__main__':
    blockchain_db = BlockchainDB()

    number_of_loops = 1010
    number_of_transactions = randint(1, 10)

    for loop in range(number_of_loops):
        for transaction in range(number_of_transactions):
            blockchain_db.add_transaction(sender=(str(uuid4()).replace('-', '')), recipient=(str(uuid4()).replace('-', '')), amount=randint(1, 10))

        blockchain_db.mine_for_next_block()

    pprint(blockchain_db.get_last_block())

