#!/usr/bin/env python3

"""
	peer.py - Blockchain P2P Networking
	Based on Daniel van Flymen's blockchain repo at: https://github.com/dvf/blockchain
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

from argparse import ArgumentParser
from uuid import uuid4

from flask import Flask, jsonify, request, render_template

from temp.blockchain import Blockchain

# Instantiate our Node with Flask
app = Flask(__name__)

# Generate a globally unique address for this node
node_ID = str(uuid4())

# Instantiate the Blockchain
blockchain = Blockchain()


"""
    VIEW
"""

@app.route('/views/chain', methods=['GET'])
def view_blockchain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return render_template('chain.html', data=response)

"""
    MODEL
"""

# Return the blockchain and its length.
@app.route('/chain', methods=['GET'])
def get_blockchain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# Add a transaction to the block.
@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    # Get request data
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to Block {0}'.format(index)}
    return jsonify(response), 201

# Mine
@app.route('/mine', methods=['GET'])
def mine():
    # Find proof of work of the last block
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.find_proof_of_work(last_proof)

    # Reward miner 1 coin
    blockchain.add_transaction(
        sender = 'Satoshi Nakamoto',
        recipient = 'Hoanh An',
        amount = 1,
    )

    # Add to the blockchain using the proof and previous hash
    previous_hash = blockchain.hash(last_block)
    block = blockchain.generate_next_block(proof, previous_hash)

    response = {
        'message': "New Block Added",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

# Register neighbouring nodes.
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # Get request data
    values = request.get_json()

    # Get list of nodes
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    # Register node for each node in the list
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

# Resolve conflict
@app.route('/nodes/resolve', methods=['GET'])
def resolve_conflict():
    is_replaced = blockchain.resolve_conflicts()

    if is_replaced:
        response = {
            'message': 'Our chain was is_replaced',
            'new_chain': blockchain.chain
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
        return jsonify(response), 200

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(port=port)