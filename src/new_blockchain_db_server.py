#!/usr/bin/env python3

"""
	new_blockchain_db_server.py - BlockchainDB Server
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 12/5/2017
"""

from flask import Flask, jsonify, render_template

from src.new_blockchain_db import BlockchainDB

app = Flask(__name__)

blockchain_db = BlockchainDB()

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Welcome to BlockchainDB")

@app.route('/views/chain', methods=['GET'])
def view_blockchain():
    response = {
        'chain': blockchain_db.get_all_blocks(),
        'length': blockchain_db.get_length(),
    }
    return render_template('chain.html', data=response)

@app.route('/views/last_blocks/<int:number>', methods=['GET'])
def view_last_n_block(number):
    # Reverse order to display latest ones to oldest one
    temp = []
    blocks = blockchain_db.get_last_n_blocks(number)
    for i in range(number, -1, -1):
        temp.append(blocks[i])

    response = {
        'chain': temp,
        'length': number,
    }
    return render_template('chain.html', data=response)

@app.route('/views/last_block', methods=['GET'])
def view_last_block():
    response = {
        'chain': [blockchain_db.get_last_block()],
        'length': 1,
    }
    return render_template('chain.html', data=response)

if __name__ == '__main__':
    app.run()