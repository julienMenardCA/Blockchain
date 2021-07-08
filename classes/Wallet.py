import uuid
import json
import glob


class Wallet:

    def __init__(self):
        self.unique_id = "00"
        self.balance = 0
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

    def sub_balance(self, value):
        self.balance -= value

    def send(self):
        pass

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
