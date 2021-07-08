import uuid
import json
import glob

from classes.Chain import Chain


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
        self.balance += value
        self.save()

    def sub_balance(self, value):
        self.balance -= value
        self.save()

    def send(self, receiver_id, amount):
        receiver_wallet = Wallet()
        receiver_wallet.load(receiver_id)
        chain = Chain()
        chain.add_transaction(self, receiver_wallet, amount)

    def save(self):
        data = {"unique_id": self.unique_id, "balance": self.balance, "history": self.history}
        with open('../content/wallets/' + self.unique_id + '.json', 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def load(self, wallet_id):
        with open('../content/wallets/' + wallet_id + '.json') as json_file:
            data = json.load(json_file)
            self.unique_id = data['unique_id']
            self.balance = data['balance']
            self.history = data['history']
