#!/usr/bin/env python3

"""
	blockchain_db_server.py - BlockchainDB Server
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""

from flask import Flask, jsonify, render_template

from src.blockchain_db import BlockchainDB

app = Flask(__name__)

blockchain_db = BlockchainDB()

@app.route('/', methods=['GET'])
def hello_world():
    """
    Welcome to Blockchain message
    :return: HTML
    """
    response = {
        'header': 'Welcome to BlockchainDB'
    }
    return render_template('landing.html', data=response)

@app.route('/view/chain', methods=['GET'])
def view_blockchain():
    """
    View the full BlockChain.
    :return: HTML
    """
    response = {
        'chain': blockchain_db.get_all_blocks(),
        'length': blockchain_db.get_length(),
        'header': 'Full chain'
    }
    return render_template('chain.html', data=response)

@app.route('/view/last_blocks/<int:number>', methods=['GET'])
def view_last_n_block(number):
    """
    View the last number of mined blocks.
    :param number: Number of blocks
    :return: HTML
    """
    # Reverse order to display latest ones to oldest one
    temp = []
    blocks = blockchain_db.get_last_n_blocks(number)
    for i in range(number - 1, -1, -1):
        temp.append(blocks[i])

    response = {
        'chain': temp,
        'length': number,
        'header': 'Last {0} Blocks'.format(number)
    }
    return render_template('chain.html', data=response)

@app.route('/view/last_block', methods=['GET'])
def view_last_block():
    """
    View the last block.
    :return: HTML
    """
    response = {
        'chain': [blockchain_db.get_last_block()],
        'length': 1,
        'header': 'Last Block'
    }
    return render_template('chain.html', data=response)

@app.route('/view/genesis_block', methods=['GET'])
def view_genesis_block():
    """
    View the genesis block.
    :return: HTML
    """
    response = {
        'chain': [blockchain_db.get_genesis_block()],
        'length': 1,
        'header': 'Genesis Block'
    }
    return render_template('chain.html', data=response)

@app.route('/view/block/<int:number>', methods=['GET'])
def view_block(number):
    """
    View a specific block for a given height number.
    :param number: Block height
    :return: HTML
    """
    response = {
        'chain': [blockchain_db.get_block(number)],
        'length': 1,
        'header': 'Block {0}'.format(number)
    }
    return render_template('chain.html', data=response)

@app.route('/view/top/<int:number>/<string:state>', methods=['GET'])
def view_top_blocks(number, state):
    """
    View a number of top blocks for a given state.
    :param number: Number of blocks
    :param state: difficulty | elapsed_time | block_reward | hash_power | height | nonce | number_of_transaction
    :return: HTML
    """
    # Reverse order to display latest ones to oldest one
    temp = []
    blocks = blockchain_db.get_top_blocks(state=state, number=number)
    for i in range(number - 1, -1, -1):
        temp.append(blocks[i])

    response = {
        'chain': temp,
        'length': number,
        'header': 'Top {0} {1}'.format(number, state)
    }
    return render_template('chain.html', data=response)

@app.route('/mine', methods=['GET'])
def mine_a_block():
    """
    Mine a block.
    :return: HTML
    """
    blockchain_db.mine_for_next_block()
    response = {
        'header': 'Successfully mined block {0}'.format(blockchain_db.get_length())
    }
    return render_template('landing.html', data=response)

@app.route('/init', methods=['GET'])
def init():
    """
    Create a genesis block.
    :return: HTML
    """
    blockchain_db.generate_genesis_block()
    response = {
        'header': 'Successfully generate a genesis block'
    }
    return render_template('landing.html', data=response)

if __name__ == '__main__':
    app.run()