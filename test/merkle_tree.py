"""
    merkle_tree.py - Merkle Tree implementations
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 12/10/17
"""

import hashlib

def find_merkle_root(transaction_ids):
    """
    Find a merle root for a given list of transaction.
    :param transaction_ids: List of transaction
    :return: Hash value
    """
    # Base case: if there is only 1 transaction, return the hash of that transaction
    if len(transaction_ids) == 1:
        return transaction_ids[0]

    # Otherwise, create a new hash list
    new_list = []

    # Go through list of transaction_ids, hash pairs of items together and add them to the new list
    for i in range(0, len(transaction_ids)-1, 2):
        new_list.append(hash_string_pair(transaction_ids[i], transaction_ids[i+1]))

    # If the length of the transaction_ids is odd, which means there is only one left over,
    # hash the last transaction with itself.
    if len(transaction_ids) % 2 == 1:
        new_list.append(hash_string_pair(transaction_ids[-1], transaction_ids[-1]))

    # Recursively do it all over again until there is one left
    return find_merkle_root(new_list)

def hash_string_pair(string_1, string_2):
    """
    Return a hash value for a given pair of string.
    :param string_1: String
    :param string_2: String
    :return: String as hash value
    """
    # Concat 2 string and encode them
    temp_string = (string_1 + string_2).encode()

    # Get the hash value
    hash_string = hashlib.sha256(temp_string).hexdigest()
    return hash_string

if __name__ == '__main__':
    transactions_id = [
        "00baf6626abc2df808da36a518c69f09b0d2ed0a79421ccfde4f559d2e42128b",
        "91c5e9f288437262f218c60f986e8bc10fb35ab3b9f6de477ff0eb554da89dea",
        "46685c94b82b84fa05b6a0f36de6ff46475520113d5cb8c6fb060e043a0dbc5c",
        "ba7ed2544c78ad793ef5bb0ebe0b1c62e8eb9404691165ffcb08662d1733d7a8",
        "a37b5e623dc26a180d9e2c9510d06885b014e86e533adb63ec40511e10b55046",
        "9dbaeb485e51d9e25a5621dc46e0bc0aaf51fb26be5acc4e370b96f62c469b80",
        "27a0797cc5b042ba4c11e72a9555d13a67f00161550b32ede0511718b22dbc2c",
    ]
    print(find_merkle_root(transactions_id))