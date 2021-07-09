import uuid
import json
import glob
import os
from datetime import datetime

import classes


class Wallet:

    def __init__(self, unique_id='00'):
        self.unique_id = unique_id
        self.balance = 100
        self.history = []

    def generate_unique_id(self):
        generated_id = str(uuid.uuid4())
        files = glob.glob('../content/wallets/*')
        while '../content/wallets\\' + generated_id + '.json' in files:
            generated_id = str(uuid.uuid4())
            files = glob.glob('../content/wallets/*')
        self.unique_id = generated_id
        return generated_id

    def add_balance(self, value):
        self.balance += int(value)
        self.save()

    def sub_balance(self, value):
        self.balance -= int(value)
        self.save()

    def send(self, receiver_id, amount):
        receiver_wallet = Wallet()
        if receiver_wallet.load(receiver_id) is True:
            chain = classes.Chain.Chain()
            if chain.add_transaction(self, receiver_wallet, amount) is True:
                transaction = {'transaction_type': 'send', 'receiver': receiver_id, 'amount': int(amount),
                               'date': datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f')}
                self.history.append(transaction)
                return True
            else:
                return 'BalanceError'
        else:
            return False

    def receive(self, sender_id, amount):
        transaction = {'transaction_type': 'receive', 'sender': sender_id, 'amount': amount,
                       'date': datetime.today().strftime('%Y-%m-%d-%H:%M:%S:%f')}
        self.history.append(transaction)

    def save(self):
        data = {"unique_id": self.unique_id, "balance": self.balance, "history": self.history}
        with open(os.getcwd() + '/content/wallets/' + self.unique_id + '.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def load(self, wallet_id):
        try:
            with open(os.getcwd() + '/content/wallets/' + wallet_id + '.json') as json_file:
                data = json.load(json_file)
                self.unique_id = data['unique_id']
                self.balance = data['balance']
                self.history = data['history']
            return True
        except FileNotFoundError:
            return False
