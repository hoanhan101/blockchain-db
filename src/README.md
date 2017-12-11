# BlockchainDB
Blockchain built on top of MongoDB.

# Design
BlockchainDB

Define a block
```
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
```



# How to test
