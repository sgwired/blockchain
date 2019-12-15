from functools import reduce
import hashlib
import json
# The reward for miners creating a new block
MINING_REWARD = 10

# The starting block of the blockchain
genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}
# Initializing our (empty) blockchain list
blockchain = [genesis_block]
# Unhandled transactions
open_transactions = []
# The owner of this blockcain node
owner = "Shelton"

# participants = set(['Max'])
participants = {"Shelton"}


def hash_block(block):
    """ Hashes a block and returns a string representation of it 
        Arguments:
            :block: the block that should be hashed
    """
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


def get_balance(participant):
    """ Calculate and return the balance for a participant """
    tx_sender = [
        [tx["amount"] for tx in block["transactions"] if tx["sender"] == participant]
        for block in blockchain
    ]
    open_tx_sender = [
        tx["amount"] for tx in open_transactions if tx["sender"] == participant
    ]
    tx_sender.append(open_tx_sender)
    amount_sent =      reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)    
    tx_recipient = [
        [tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant]
        for block in blockchain
    ]
    amount_received =  reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    return amount_received - amount_sent


def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value to the 
    blockchain 
    
    Arguments:
        :sender The sender of the coin.
        :recipient: The recipient of the coin 
        :recipient: The amount of coins sent with transaction (default[1])
    """
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    if verify_transaction(transaction):

        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = ""
    hashed_block = hash_block(last_block)
    print(hashed_block)
    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD,
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions,
    }
    blockchain.append(block)
    return True


def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float """
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount please: "))
    return (tx_recipient, tx_amount)


def get_user_choice():
    return input("Your choice: ")


def print_blockchain_elements():
    """ Output the elements of the blockchain """
    for block in blockchain:
        print("Outputting Block")
        print(block)
    else:
        print("-" * 20)


def verify_chain():
    """ Verify the current blockchain and return True if Valid """
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True
while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Output participants")
    print("5: Check transaction validity")
    print("h: Manipulate the chain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Added transaction")
        else:
            print("Transaction Failed")
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [
                    {"sender": "Chris", "recipient": "Max", "amount": 100.0}
                ],
            }
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input was invalid, please pick value from the list")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain")
        break
    print('Balance of {}: {:6.2f}'.format('Shelton', get_balance("Shelton")))
else:
    print("User left!")
print("Done")
