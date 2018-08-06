class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Starting block when the an instance is created
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """ create and add a new block to the chain
        proof parameter is given to us by the Proof of Work algorithm
        previous_hash is by default set to none
        """
        #block
        pass

    def new_transaction(self, sender, recipient, amount):
        # add a new transaction to the transaction list
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        # hash the block
        pass

    @property
    def last_block(self):
        # return the last block in th chain
        pass
