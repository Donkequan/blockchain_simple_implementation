import json
from argparse import ArgumentParser

from flask import Flask, request, jsonify
import requests
from block import *
from blockchain import *



# Initialize flask application
app = Flask(__name__)

# Initialize a blockchain object.
blockchain = Blockchain()

# Contains the host addresses of other participating members of the network
peers = list()

current_port = 8080


# 上传一个交易， 需要被client的submit_tx函数调用
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    tx_data["timestamp"] = time.time()
    blockchain.add_new_transaction(tx_data)
    return tx_data


# 返回节点完整的链结构
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data), "chain": chain_data})


# 调用blockchain的generate_block，挖矿，并且把块添加到区块链中
@app.route('/generate_block', methods=['GET'])
def mine_unconfirmed_transactions():
    # 返回新块
    new_block = blockchain.generate_block()
    if not new_block:
        return "ERROR"
    announce_new_block(new_block)
    return f"Block #{new_block.index} is mined."


# 返回未打包到块中的交易
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


# add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()
    print(node_address)
    peers.append(node_address)
    # 返回链长度和数据
    return get_chain()


#加入到目标节点
@app.route('/join/<string:ip>/<int:port>', methods=['GET'])
def add_nodes(ip, port):
    join_node = {"ip": "localhost", "port": current_port}
    server_interface = "/register_node"
    # 得到链长度和数据
    print(f"{ip}:{port}")
    response = requests.post(f"http://{ip}:{port}{server_interface}",
                             json=join_node,
                             headers={'Content-type': 'application/json'})
    length = response.json()['length']
    new_chain = response.json()["chain"]
    print(f"new_chain: {new_chain}")
    if length >= len(blockchain.chain):
        blockchain.chain.clear()
        print(f"new_chain2: {new_chain}")
        create_chain_from_dic(new_chain)
    peers.append({"ip": ip, "port": port})
    print(blockchain)
    return "ok"


#加入到目标节点
@app.route('/peers', methods=['GET'])
def get_peers():
    return str(peers)


# 复制chain
def create_chain_from_dic(chain_dic):
    for block_data in chain_dic:
        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data['nonce'])
        block.hash = block_data['hash']
        if block_data["index"] > 0:
            added = blockchain.add_block(block, block_data['hash'])
            if not added:
                raise Exception("The chain dump is tampered!!")
        else:
            blockchain.chain.append(block)

# 如果一个长链被发现，我们的就被替代
@app.route('/consensus', methods=['GET'])
def consensus():
    global blockchain
    longest_chain = None
    current_len = len(blockchain.chain)
    for peer in peers:
        print("进入了1")
        ip = peer["ip"]
        port = peer["port"]
        url = f"http://{ip}:{port}/chain"
        response = requests.get(url)
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            print("进入了")
            current_len = length
            longest_chain = chain
    if longest_chain:
        blockchain.chain.clear()
        create_chain_from_dic(longest_chain)
        print(f"longest_chain: {longest_chain}")
    return get_chain()


@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = eval(request.get_json())
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data['nonce'])
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)
    if not added:
        return "The block was discarded by the node", 400
    return "Block added to the chain", 201

# announce to the network once a block has been mined.
def announce_new_block(block):
    for peer in peers:
        ip = peer["ip"]
        port = peer["port"]
        url = f"http://{ip}:{port}/add_block"
        print(f"block: {block}")
        print(f"block: {block.__dict__}")
        requests.post(url, json=json.dumps(block.__dict__, sort_keys=True), headers={'Content-type': 'application/json'})

# 爬取链数据
def fetch_posts():
    get_chain_address = f"localhost:{current_port}/chain"
    response = requests.get(get_chain_address)
    if response.status_code == 200:
        contentTX = []
        chain = json.loads(response.content)
        for block in chain["chain"]:
            for tx in block["transactions"]:
                tx["index"] = block["index"]
                tx["hash"] = block["previous_hash"]
                contentTX.append(tx)
        # 按时间降序排序
        return sorted(contentTX, key=lambda k: k['timestamp'], reverse=True)

@app.route('/')
def index():
    sortedTX = fetch_posts
    return f"transaction: {sortedTX},\n" \
           f"server: localhost:{current_port},\n" \
           f"time: {time.time()}"


if __name__ =="__main__":
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    current_port = args.port
    app.run(debug=True, host='0.0.0.0', port=current_port)