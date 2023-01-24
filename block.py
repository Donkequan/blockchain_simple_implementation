from hashlib import sha256
import json
import time


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def __str__(self):
        msg = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.compute_hash()
        }
        return str(msg)

    def to_dic(self):
        msg = {
            "index": self.index,
            "transactions": str(self.transactions),
            "timestamp":  self.timestamp,
            "previous_hash":  str(self.previous_hash),
            "nonce": self.nonce
        }
        return msg

    def compute_hash(self):
        block_string = json.dumps(self.to_dic(), sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    # @property
    # def hash(self):
    #     block_string = json.dumps(self.__dict__, sort_keys=True)
    #     return sha256(block_string.encode()).hexdigest()


