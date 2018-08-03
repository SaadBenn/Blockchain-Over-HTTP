class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # create and add a new block to the chain
        pass

    def new_transaction(self):
        # add a new transaction to the transaction list
        pass

    @staticmethod
    def hash(block):
        # hash the block
        pass

    @property
    def last_block(self):
        # return the last block in th chain
        pass
