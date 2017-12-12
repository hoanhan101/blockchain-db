#!/usr/bin/env python3

"""
	blockchain_db_test.py - BlockchainDB Test
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""

from src.blockchain_db import BlockchainDB
from pprint import pprint
from uuid import uuid4
from random import randint

import random

if __name__ == '__main__':
    # blockchain_db = BlockchainDB()
    # blockchain_db.reset()

    """
        Mining blocks
    """
    # number_of_loops = 1010
    # for loop in range(number_of_loops):
    #     for transaction in range(randint(1, 50)):
    #         blockchain_db.add_transaction(sender=(str(uuid4()).replace('-', '')[:-10]),
    #                                       recipient=(str(uuid4()).replace('-', '')[:-10]),
    #                                       amount=round(random.uniform(1, 10), 2))
    #
    #     blockchain_db.mine_for_next_block()


    # pprint(blockchain_db.get_last_block())
