# blockchain simple implementation in Python

A simple implementation for developing a blockchain application with mining in Python.

项目是一个区块链的简单实现，是支持数据上传，挖矿和共识。

为了简化，没有加入签名认证，并且实验时一次只能有一个节点挖矿。

<br>

**必要环境**

- python3

基于Flask框架和requests请求

```cmd
pip3 install -r requirements.txt
```

<br>

**功能实现和测试**：

1. **交易上传**

   ```pcmd
   python flask_server.py -p 8080
   python client.py -p 8080 -a hdk -d hhhhhh
   ```

   访问：

   ```
   localhost:8080/pending_tx
   ```

   输出：
   
   ```json
   [{"author": "hdk", "content": "hhhhhh", "timestamp": 1674557970.5027435}]
   ```

2. **挖块**

   ```pcmd
   访问：
   localhost:8080/generate_block
   localhost:8080/chain
   ```

   输出链结构：

   ```json
   {"length": 2, "chain": [{"index": 0, "transactions": [], "timestamp": 1674557968.4578717, "previous_hash": "0", "nonce": 0, "hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173"}, {"index": 1, "transactions": [{"author": "hdk", "content": "hhhhhh", "timestamp": 1674557970.5027435}], "timestamp": 1674558249.506999, "previous_hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173", "nonce": 761, "hash": "00006de85025cab6ee8bc33dc34c7dad21489c8c1363836113766e6eb1226d07"}]}
   ```

3. **节点加入**

   ```cmd
   python .\flask_server.py -p 8081
   ```

   端口8081加入8080的网络

   ```url
   localhost:8081/join/localhost/8080
   ```

   查看8080端口加入的节点：

   ```json
   浏览器访问：localhost:8080/peers
   [{'ip': 'localhost', 'port': 8081}]
   ```
   查看8081端口加入的节点
   
   ```json
   浏览器访问：localhost:8080/peers
   返回：[{'ip': 'localhost', 'port': 8081}]
   ```
   
   查看8080端口块数据
   
   ```json
   浏览器访问：localhost:8080/chain
   返回：{"length": 2, "chain": [{"index": 0, "transactions": [], "timestamp": 1674557968.4578717, "previous_hash": "0", "nonce": 0, "hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173"}, {"index": 1, "transactions": [{"author": "hdk", "content": "hhhhhh", "timestamp": 1674557970.5027435}], "timestamp": 1674558249.506999, "previous_hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173", "nonce": 761, "hash": "00006de85025cab6ee8bc33dc34c7dad21489c8c1363836113766e6eb1226d07"}]}
   ```
   
   查看8081端口块数据
   
   ```json
   浏览器访问：localhost:8081/chain
   返回：{"length": 2, "chain": [{"index": 0, "transactions": [], "timestamp": 1674557968.4578717, "previous_hash": "0", "nonce": 0, "hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173"}, {"index": 1, "transactions": [{"author": "hdk", "content": "hhhhhh", "timestamp": 1674557970.5027435}], "timestamp": 1674558249.506999, "previous_hash": "1857515eb50c52193140126226825e0a8203488afa70b2b21a407cb45c0e4173", "nonce": 761, "hash": "00006de85025cab6ee8bc33dc34c7dad21489c8c1363836113766e6eb1226d07"}]}
   ```

​		块数据一致

<br>

<br>

Ref：

https://github.com/OpensourceBooks/blockchain

https://github.com/satwikkansal/python_blockchain_app/tree/ibm_blockchain_post
