import hashlib
import glob

from classes.Block import Block
from classes.Wallet import Wallet


class Chain:

    def __init__(self):
        self.blocks = ['00']
        self.last_transaction_number = 0
        self.hash_number = -1

    def generate_hash(self):
        generated_hash = hashlib.sha256(self.num_to_hash().encode()).hexdigest()
        while self.verify_hash(generated_hash) is not True:
            generated_hash = hashlib.sha256(self.num_to_hash().encode()).hexdigest()
        return generated_hash

    @staticmethod
    def verify_hash(generated_hash):
        files = glob.glob('../content/blocks/*')
        if '../content/wallets\\' + generated_hash + '.json' not in files and generated_hash[:4] == '0000':
            return True
        else:
            return False

    def add_block(self):
        block_hash = self.generate_hash()
        block = Block(self.hash_number, block_hash, self.blocks[-1])
        self.blocks.append(block_hash)
        return block

    @staticmethod
    def get_block(block_hash):
        block = Block()
        block.load(block_hash)
        return block

    def add_transaction(self, sender_wallet: Wallet, receiver_wallet: Wallet, amount):
        # TODO better implementation of weight
        block = Block()
        block.load(self.blocks[-1])
        if block.get_weight() >= 255999:
            block = self.add_block()
        block.add_transaction(sender_wallet, receiver_wallet, amount)
        self.last_transaction_number += 1

    def num_to_hash(self):
        self.hash_number += 1
        return str(self.hash_number)
