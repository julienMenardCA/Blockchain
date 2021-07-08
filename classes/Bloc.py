import json
import os

from classes.Wallet import Wallet


class Bloc:

    def __init__(self):
        self.base_hash = 0
        self.hash = '00'
        self.parent_hash = ''
        self.transactions = []

    def check_hash(self):
        pass

    def add_transaction(self, sender_wallet: Wallet, receiver_wallet: Wallet, amount):
        sender_wallet.sub_balance(amount)
        receiver_wallet.add_balance(amount)

    def get_transaction(self, num_transaction):
        pass

    def get_weight(self):
        return os.stat('../content/blocs/' + self.hash + '.json').st_size

    def save(self):
        data = {"hash": self.hash, "parent_hash": self.parent_hash, "transactions": self.transactions}
        with open('../content/blocs/' + self.hash + '.json', 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def load(self, bloc_hash):
        with open('../content/wallets/' + bloc_hash + '.json') as json_file:
            data = json.load(json_file)
            self.hash = data['hash']
            self.parent_hash = data['parent_hash']
            self.transactions = data['transactions']