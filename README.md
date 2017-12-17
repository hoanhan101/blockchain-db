# BlockchainDB
Blockchain + MongoDB = BlockchainDB

## Design

### `blockchain_db.py`
This file contains the main BlockchainDB's logic. I am using `pymongo` to connect with mongodb
database named `blockchain` and the `block` collection. Whenever a new bock is mined, it will
write to the database.  

#### Main methods
- `generate_genesis_block()`
- `generate_next_block(nonce, previous_hash=None)`
- `add_transaction(sender, recipient, amount)`
- `find_merkle_root(transaction_ids)`
- `mine_for_next_block()`
- `calculate_nonce(last_block, number_of_bits)`
- `calculate_block_reward()`
- `calculate_difficulty_bits()`
- `calculate_difficulty()`
- `hash_json_object(json_object)`
- `hash_string_pair(string_1, string_2)`

#### `GET`
- `get_length()`
- `get_last_n_blocks(number)`
- `get_top_blocks(state, number)`
- `get_last_block()`
- `get_genesis_block()`
- `get_block(height)`
- `get_all_blocks()`
- `get_transaction_ids()`

### `blockchain_db_server.py`
This use `Flask` to serve as a web page. 

### Available endpoints
- Drop the database and create a genesis block: `/reset`
- Mine a number of blocks over network: `/mine/<int:number>`
- View the full BlockChain: `/view/chain`
- View some number of last mined blocks: `/view/last_blocks/<int:number>`
- View the last mined block: `/view/last_block`
- View the genesis block: `/view/genesis_block`
- View a specific block: `/view/block/<int:number>`
- View top numbers of blocks for a given state:`/view/top/<int:number>/<string:state>`

## How to test
#### Option 1: With networking.
- Start `blockchain_db_server.py` as a starting web page.
- Go to `/reset` to create a genesis block. This endpoints can also be used to drop the database
and start over whenever you want to.
- Mine some blocks at `/mine/<int:number>`
- Use available `/view` endpoints as mentioned above for visualization.

#### Option 2: Without networking.
- Start `blockchain_db_test.py` to create an instance of BlockchainDB to mine some blocks.
- Execute `reset()` only once when you start to drop the old database and create a genesis block.
- Comment it out after the second run and try to mine some blocks with the testing script.
- Start `blockchain_db_server.py` to serve as a web page and view the result on the web or just
print it using the console.  

## Docker
- Work in process. Having difficulty connecting to mongodb database.

## TODO
- Dockerize everything
- Introduce networking with multiple nodes. For now, it only works with one node, which is
the local host.
- Introduce Wallet
- Introduct attack.
