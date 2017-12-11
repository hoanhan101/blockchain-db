# BlockchainDB
Blockchain built on top of MongoDB.

## Design

### `blockchain_db.py`
Main BlockchainDB's logic, using `MongoClient`.

#### Main methods
- `generate_genesis_block(self)`
- `generate_next_block(self, nonce, previous_hash=None)`
- `generate_next_block(self, nonce, previous_hash=None)`
- `add_transaction(self, sender, recipient, amount)`
- `find_merkle_root(self, transaction_ids)`
- `mine_for_next_block(self)`
- `calculate_nonce(self, last_block, number_of_bits)`

#### Helper functions
- `calculate_block_reward(self)`
- `calculate_difficulty_bits(self)`
- `calculate_difficulty(self)`
- `hash_json_object(self, json_object)`
- `hash_string_pair(self, string_1, string_2)`

#### `GET`
- `get_length(self)`
- `get_last_n_blocks(self, number)`
- `get_top_blocks(self, state, number)`
- `get_last_block(self)`
- `get_genesis_block(self)`
- `get_block(self, height)`
- `get_all_blocks(self)`
- `get_transaction_ids(self)`

### `blockchain_db_server.py`
Server as a web page using `Flask`.

### APIs
- View the full BlockChain: `/view/chain`
- View some number of last mined blocks: `/view/last_blocks/<int:number>`
- View the last mined block: `/view/last_block`
- View the genesis block: `/view/genesis_block`
- View a specific block: `/view/block/<int:number>`
- View top numbers of blocks for a given state:`/view/top/<int:number>/<string:state>`
- Mine a block over network: `/mine`
- Docker WIP: `/init`


## Docker
- Work in process

## How to test
- Use `blockchain_db_test.py` to create an instance of BlockchainDB to mine some blocks.
- Create a genesis block first, can uncomment and execute line 42 `self.generate_genesis_block()` in `blockchain_db.py`
to do the trick. **Remember to uncomment before the second run if you do this!** Otherwise you would not run.
- *TODO: FInd better way for to handle this. Probably along with Docker.*
- Run `blockchain_db_server.py` to serve as a web page and try out different endpoints. 
