import hashlib
import time, datetime, copy
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.difficulty = 3
        self.minerRewards = 50
        self.blocksize = 10

    def minePendingTransaction(self, miner):
        lenPT = len(self.pendingTransactions)

        for i in range(0, lenPT, self.blocksize):
            end = i + self.blocksize
            if(i>=lenPT):
                end=lenPT

            transactionSlice = self.pendingTransactions[i:end]

            newBlock = Block(transactionSlice, time.time(), len(self.chain))
            hashVal = self.getLastBlock().hash
            newBlock.prev = hashVal
            newBlock.mineBlock(self.difficulty)
            self.chain.append(newBlock)
        print("Mining Transactions Success!")

    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block):
        if(len(self.chain) > 0):
            block.prev = self.getLastBlock().hash
        else:
            block.prev = "none"
        self.chain.append(block)

    def chainJSONencode(self):
        blockArrJSON = []

        for block in self.chain:
            blockJSON = {}
            blockJSON["hash"] = block.hash
            blockJSON["prev"] = block.prev
            blockJSON["transactions"] = block.transactions
            blockArrJSON.append(blockJSON)

        return blockArrJSON
            

class Block(object):
    def __init__(self, transactions, time, index):
        self.index = index # block number
        self.transactions = transactions
        self.time = time  # time the block is created
        self.prev = ""
        self.hash = self.calculateHash();
        self.nonse = 0


    def mineBlock(self, difficulty):
        arr = []
        for i in range(0, difficulty):
            arr.append(i)

        arrStr = map(str, arr)
        hashPuzzle = "".join(arrStr)
        while(self.hash[0:difficulty] != hashPuzzle):
            self.nonse += 1
            self.hash = self.calculateHash()
            print("Nonse:", self.nonse)
            print("hash attempt:", self.hash)
            print("Hash We Want:", hashPuzzle, "...")
            print("")
            time.sleep(0.8)
        print("")
        print("Block Mined! Nonse to solve proof of work: ", self.nonse)
        return True

    def calculateHash(self):
        hashTransactions = ""
        for transaction in self.transactions:
            hashTransactions += transaction.hash

        hashString = str(self.time) + hashTransactions + self.prev + str(self.index)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
        

class Transaction(object):
    def __init__(self, sender, reciever, amt):
        self.sender = sender
        self.reciever = reciever
        self.amt = amt
        self.time = time.time()
        self.hash = self.calculateHash()

    def calculateHash(self):
        hashString = self.sender + self.reciever + str(self.amt) + str(self.time)
        hashEncoded = json.dumps(hashString, sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()


if __name__=="__main__":
    blockchain = Blockchain()
    transactions = []

    block = Block(transactions, time.time(), 0)
    blockchain.addBlock(block)

    block = Block(transactions, time.time(), 1)
    blockchain.addBlock(block)

    pp.pprint(blockchain.chainJSONencode())
    print("Length: ", len(blockchain.chain))
