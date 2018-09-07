import time
import hashlib
import json
# generate random objects of 128 bits as IDs
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        """
        Constructor for creating an instance of Blockchain class
        """
        self.chain = []
        self.current_transactions = []

        # Starting block when an instance is created
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        create and add a new block to the chain
        proof parameter is given to us by the Proof of Work algorithm
        previous_hash is by default set to none
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': self.hash(self.chain() - 1) or previous_hash,
        }
        # reset the transactions for the new block
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        add a new transaction to the transaction list
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Proof of work aka HASHCASH: simple implementation
        We will find a number p (new proof) that when hashed hash(p,last_proof) gives us a hash with 4 leading zeros
        the new hash (p) will start with 0
        """

        new_proof = 0
        while self.valid_proof(last_proof, new_proof) is False:
            new_proof += 1

        return new_proof

    @staticmethod
    def valid_proof(last_proof, new_proof):
        """
        return true if the hash contains 4 leading zeros otherwise false
        """

        guess = f'{last_proof, new_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        returns a string representation of the json object from a dictionary (sort them for consistent hashes)
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        return the last block in th chain
        """
        return self.chain[-1]


# *****************************************************************************
#                   Flask boilerplate code
# *****************************************************************************

# server will be a single node
app = Flask(__name__)

# get a unique identifier
unique_node_identifier = str(uuid4()).replace('-', '')

# get an instance of Blockchain class
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    Get the new proof by invoking the proof of work algorithm
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    new_proof = blockchain.proof_of_work(last_proof)

    # reward the miner - "sender=0" signifies the mining of a new a coin
    # For simplicity - the recipient is the address of the node
    blockchain.new_transaction(
        sender='0',
        recipient=unique_node_identifier,
        amount=1,
    )

    # add the new block to the chain
    prev_hash = blockchain.hash(last_block)
    block = blockchain.new_block(new_proof, prev_hash)

    response = {
        'message': 'Block added',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['new_proof'],
        'prev_hash': block['prev_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():

    values = request.get_json(force=True)

    required = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required):
        return 'Missing fields', 400

    transaction_index = blockchain.new_transaction(values['sender'], ['recipient'], ['amount'])
    response = {'message': f'Transaction to be added {transaction_index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def get_chain():
    result = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000)
