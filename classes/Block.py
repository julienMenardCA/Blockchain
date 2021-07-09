import json
import os
import hashlib

from classes.Wallet import Wallet


class Block:

    def __init__(self, base_hash=0, block_hash='00', parent_hash='00'):
        self.base_hash = base_hash
        self.hash = block_hash
        self.parent_hash = parent_hash
        self.transactions = []

    def check_hash(self):
        str_base_hash = str(self.base_hash)
        if hashlib.sha256(str_base_hash.encode()).hexdigest() == self.hash:
            return True
        else:
            return False

    def add_transaction(self, sender_wallet: Wallet, receiver_wallet: Wallet, amount, transaction):
        sender_wallet.sub_balance(amount)
        receiver_wallet.add_balance(amount)
        receiver_wallet.receive(receiver_wallet.unique_id, amount)
        transaction['num_transaction'] = len(self.transactions) + 1
        self.transactions.append(transaction)
        self.save()

    def get_transaction(self, num_transaction):
        index = self.transactions.index({'num_transaction': num_transaction})
        return self.transactions[index]

    def get_weight(self):
        return os.stat('../content/blocks/' + self.hash + '.json').st_size

    def save(self):
        data = {"hash": self.hash, "parent_hash": self.parent_hash, "transactions": self.transactions}
        with open('../content/blocks/' + self.hash + '.json', 'w', encoding='utf8') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def load(self, block_hash):
        try:
            with open('../content/blocks/' + block_hash + '.json') as json_file:
                data = json.load(json_file)
                self.hash = data['hash']
                self.parent_hash = data['parent_hash']
                self.transactions = data['transactions']
        except FileNotFoundError:
            return False
