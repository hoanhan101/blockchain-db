# Blockchain

## Methods
- `__init__(self)`
- `generate_next_block(self, proof, previous_hash=None)`
- `add_transaction(self, sender, recipient, amount)`
- `find_proof_of_work(self, last_proof)`
- `register_node(self, address)`
- `verify_chain(self, chain)`
- `resolve_conflicts(self)`
- `verify_proof_of_work(last_proof, proof)`
- `hash(block)`
- `last_block(self)`

## REST APIs
- Return the blockchain and its length: `/chain`
- Add a transaction to the block: `/transactions/new`
- Mine: `/mine`
- Register neighbouring nodes: `/nodes/register`
- Resolve conflict: `/nodes/resolve`

## How to test
- `$ python3 peer.py` runs in default port 5000
- `$ python3 peer.py -p 5001` runs in port 5001
- `$ python3 test.py`