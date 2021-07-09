from classes.Wallet import Wallet


def transaction(w):
    receiver = ''
    amount = ''
    sendResponse = w.send(receiver, amount)
    while sendResponse is not True:
        receiver = input("Please enter the valid id of the receiving wallet : ")
        amount = input("Please enter the amount of tokens you want to send : ")
        sendResponse = w.send(receiver, amount)
        if sendResponse is True:
            print(amount + ' tokens where sent to wallet id : ' + receiver)
        elif sendResponse == 'BalanceError':
            print("Not enough tokens in balance")
        else:
            print("Wrong wallet id")


def walletManage(w):
    answer = ''
    print("\nHere is your wallet management area\nYour current balance is : " + str(w.balance))
    while answer != 'q':
        answer = input("Please enter a command (type 'h' for a list of commands) : ")
        if answer == 'h':
            print("Type 'c' to check your wallet balance\n"
                  "Type 's' to see your transactions history\n"
                  "Type 't' to make a transaction to another wallet\n"
                  "Type 'q to quit your wallet")
        elif answer == 'c':
            print("Your current balance is : " + str(w.balance))
        elif answer == 's':
            print(w.history)
        elif answer == 't':
            transaction(w)
        elif answer == 'q':
            print("You're exiting your wallet")
        else:
            print("Unknown command.\n")


def walletConnect():
    uid = ''
    w = Wallet()
    while w.load(uid) is not True:
        uid = input("Enter your wallet id to connect : ")
        if w.load(uid):
            print("Connection to your wallet successful")
            walletManage(w)
        else:
            print("Connection to your wallet failed")


def walletCreate():
    w = Wallet()
    w.generate_unique_id()
    w.save()
    print("Wallet successfully created !\n")
    print("Here is you wallet id : " + w.unique_id + "\nWrite it somewhere safe to not lose it")
    walletManage(w)


def wallet():
    answer = ''
    print("\nWallet connection/creation ('q' to quit)")
    while answer != 'q':
        answer = input("Do you already have a wallet ? (y/n) : ")
        if answer == 'y':
            walletConnect()
        if answer == 'n':
            while answer != 'q':
                answer = input("Do you want to make a wallet ? (y/n) : ")
                if answer == 'y':
                    walletCreate()
                if answer == 'n':
                    print("Well ok then")
                else:
                    print("Unknown command.\n")
        elif answer == 'q':
            print("You're exiting Wallet connection/creation")
        else:
            print("Unknown command.\n")


def main():
    answer = ''
    print("Hello and welcome to the Best BlockChain Evert™!")
    while answer != 'q':
        answer = input("Please enter a command (type 'h' for a list of commands) : ")
        if answer == 'h':
            print("Type 'w' to access your wallet or create one if don't already have and 'q' to quit\n")
        elif answer == 'w':
            wallet()
        elif answer == 'q':
            print("Goodbye !!! ^_^")
        else:
            print("Unknown command.\n")


if __name__ == "__main__":
    main()
