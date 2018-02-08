# blockchain-db
Blockchain + MongoDB = BlockchainDB, aka blockchain-db

## Files and structure

### `blockchain_db.py`
This file contains the main BlockchainDB's logic. I am using `pymongo` to connect with mongodb
database named `blockchain` and the `block` collection. Whenever a new bock is mined, it will
write to the database.  

#### Block structure
```JSON
block = {
    "previous_block": str,
    'height': int,
    'timestamp': unix time,
    'transactions': list,
    "merkle_root": str,
    'number_of_transaction': int,
    'nonce': int,
    'previous_hash': str,
    'block_reward': int,
    'difficulty_bits': int,
    'difficulty': int,
    'elapsed_time': int,
    'hash_power': int 
}
```

#### Here are the main methods, details are well documented in doctrings.
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

#### Supported GET methods
- `get_length()`
- `get_last_n_blocks(number)`
- `get_top_blocks(state, number)`
- `get_last_block()`
- `get_genesis_block()`
- `get_block(height)`
- `get_all_blocks()`
- `get_transaction_ids()`

### `blockchain_db_server.py`
This file uses `Flask` to serve as a web page. 

### APIs
Endpoint | Description
--- | ---
`/reset` | Drop the database and create a genesis block
`/mine/<int:number>` | Mine a number of blocks over network
`/view/chain` | View the full BlockChain
`/view/last_blocks/<int:number>` | View some number of last mined blocks
`/view/last_block` | View the last mined block 
`/view/genesis_block` | View the genesis block
`/view/block/<int:number>` | View a specific block
`/view/top/<int:number>/<string:state>` | View top numbers of blocks for a given state

## Usage

#### Option 1: With networking.
- In `src`, start `blockchain_db_server.py` and visit `localhost:5000`
- Hit `/reset` endpoint to create a genesis block. This endpoints can also be used to drop the database
and start over whenever you want to.
- Mine some number of blocks at `/mine/<int:number>`
- Use available `/view` endpoints as mentioned above for more details.

#### Option 2: Without networking.
- In `test`, start `blockchain_db_test.py` to create an instance of BlockchainDB to mine some blocks.
- Execute `reset()` only once when you start to drop the old database and create a genesis block.
- Comment it out after the second run and try to mine some blocks with the provided testing script.
- Similar to the first option, start `blockchain_db_server.py` in `src` to serve as a web page and view the result on the web
or just print it using the console.  

## Docker
- Work in process. Having difficulty connecting to mongodb database.

## TODO
- Dockerize everything
- Introduce networking with multiple nodes. For now, it only works with one node, which is the local host.
- Introduce Wallet
- Introduct attack.
