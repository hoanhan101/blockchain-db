"""
    new_blockchain.py
"""

block = {
    "previous_block": 1,
    "height": 2,
    "hash": "101",
    "previous_hash": "102",
    "number_of_transaction": 10,
    "block_reward": 1,
    "timestamp": 1231006505,
    "miner": "Hoanh An",
    "transactions": [
        "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    ],
    "merkle_root": "hash_of_all transactions",
    "nonce": 2083236893,
    "difficulty": 1.00000000,
}

model_a_block = {
    "previous_block": get_previous_block(),
    "height": get_height(),
    "hash": get_hash(),
    "previous_hash": get_previous_hash(),
    "number_of_transaction": get_number_of_transactions(),
    "block_reward": get_block_reward(),
    "miner": get_miner(),
    "transactions": get_transactions(),
    "merkle_root": get_merkle_root(),
    "nonce": get_nonce(),
    "difficulty": get_difficulty()
}

def get_previous_block():
    pass

def get_height():
    # return index
    pass

def get_hash():
