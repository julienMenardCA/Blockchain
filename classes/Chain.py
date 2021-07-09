import hashlib
import glob
import json
import os
from datetime import datetime

import classes


class Chain:

    def __init__(self):
        self.blocks = ['00']
        self.last_transaction_number = 0
        self.hash_number = -1
        self.str_hashed = ''

    def generate_hash(self):
        generated_hash = hashlib.sha256(self.str_to_hash().encode()).hexdigest()
        while self.verify_hash(generated_hash) is not True:
            generated_hash = hashlib.sha256(self.str_to_hash().encode()).hexdigest()
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
        block = classes.Block.Block(self.str_hashed, block_hash, self.blocks[-1])
        self.blocks.append(block_hash)
        return block

    @staticmethod
    def get_block(block_hash):
        block = classes.Block.Block()
        block.load(block_hash)
        return block

    def add_transaction(self, sender_wallet, receiver_wallet, amount):
        if sender_wallet.balance >= int(amount):
            transaction = {'num_transaction': '', 'sender': sender_wallet.unique_id,
                           'receiver': receiver_wallet.unique_id,
                           'amount': int(amount),
                           'date': datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f')}
            block = classes.Block.Block()
            if self.blocks[-1] == '00':
                listOfFiles = os.listdir(os.getcwd() + '/content/blocks/')
                listOfBlocksFromFiles = [x.split('.')[0] for x in listOfFiles]
                self.blocks += listOfBlocksFromFiles[1:]
                block = self.add_block()
                block.save()
            block.load(self.blocks[-1])
            if block.get_weight() + len(json.dumps(transaction).encode('utf8')) > 256000:
                block = self.add_block()
                block.save()
            block.add_transaction(sender_wallet, receiver_wallet, amount, transaction)
            self.last_transaction_number += 1
            return True
        else:
            return False

    def str_to_hash(self):
        date = datetime.today().strftime('%Y%m%d%H%M%S%f')
        if self.hash_number <= 999999999:
            self.hash_number += 1
        else:
            self.hash_number = -1
        self.str_hashed = str(self.hash_number) + date
        return self.str_hashed
