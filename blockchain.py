from block import *


class Blockchain:

    # difficulty of PoW algorithm
    difficulty = 4

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def __str__(self):
        return f"chain: {self.chain}"

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    # 索引最近的块
    @property
    def last_block(self):
        return self.chain[-1]

    # 执行挖矿算法
    def mine(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof_hash):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            print("hash不相同")
            return False
        if not self.is_valid_proof(block, proof_hash):
            print("难度不符合")
            return False
        block.hash = proof_hash
        self.chain.append(block)
        return True

    # 检查hash是否符合挖矿规则
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
            block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # 挖矿，并且把块添加到区块链中
    def generate_block(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof_hash = self.mine(new_block)
        if self.add_block(new_block, proof_hash):
            self.unconfirmed_transactions = []
        # print(len(self.chain))
            return new_block
        return False

    # 检查完整的区块链是否有效
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"
        for block_data in chain:
            block = Block(block_data["index"],
                          block_data["transactions"],
                          block_data["timestamp"],
                          block_data["previous_hash"],
                          block_data["nonce"])
            proof = block_data['hash']
            if block.index > 0:
                if not cls.is_valid_proof(block, proof) or \
                        previous_hash != block.previous_hash:
                    print("区块链问题")
                    return False
            block.hash, previous_hash = proof, proof
        return result


