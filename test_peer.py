#!/usr/bin/env python3

"""
	test_peer.py - Unit Test P2P Networking
	Author: Hoanh An (hoanhan@bennington.edu)
	Date: 11/26/2017
"""

import requests, unittest, json

class TestSinglePeer(unittest.TestCase):
    def test_get_chain(self):
        r = requests.get('http://0.0.0.0:5000/chain')
        self.assertEqual(200, r.status_code)

    def test_mine(self):
        r = requests.get('http://0.0.0.0:5000/mine')
        self.assertEqual(200, r.status_code)

    def test_resolve_conflict(self):
        r = requests.get('http://0.0.0.0:5000/nodes/resolve')
        self.assertEqual(200, r.status_code)

    def test_add_transaction(self):
        package = {
            "sender": "d4ee26eee15148ee92c6cd394edd974e",
            "recipient": "someone-other-address",
            "amount": 5
        }
        r = requests.post('http://0.0.0.0:5000/transactions/new', json=package)
        self.assertEqual(201, r.status_code)

    def test_register_node(self):
        package = {
            "nodes": ["http://127.0.0.1:5001"]
        }
        r = requests.post('http://0.0.0.0:5000/nodes/register', json=package)
        self.assertEqual(201, r.status_code)

class TestTwoPeers(unittest.TestCase):
    def test_get_chain(self):
        r1 = requests.get('http://0.0.0.0:5000/chain')
        r2 = requests.get('http://0.0.0.0:5001/chain')
        self.assertEqual(200, r1.status_code)
        self.assertEqual(200, r2.status_code)

    def test_mine(self):
        r1 = requests.get('http://0.0.0.0:5000/mine')
        r2 = requests.get('http://0.0.0.0:5001/mine')
        self.assertEqual(200, r1.status_code)
        self.assertEqual(200, r2.status_code)

    def test_resolve_conflict(self):
        peer_2_package = {
            "nodes": ["http://127.0.0.1:5000"]
        }
        peer_2_regis = requests.post('http://0.0.0.0:5001/nodes/register', json=peer_2_package)

        peer_1_mine_1 = requests.get('http://0.0.0.0:5000/mine')
        peer_1_mine_2 = requests.get('http://0.0.0.0:5000/mine')
        peer_1_mine_3 = requests.get('http://0.0.0.0:5000/mine')

        peer_2_resolve = requests.get('http://0.0.0.0:5001/nodes/resolve')
        self.assertEqual(201, peer_2_resolve.status_code)

if __name__ == '__main__':
    unittest.main()
