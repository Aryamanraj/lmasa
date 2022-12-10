from crypt import methods
import datetime
import hashlib
import json
from django.dispatch import receiver
from flask import Flask, jsonify, request
import string
import random

responser = []
class Blockchain:
    
    def __init__(self):
        self.chain = []

        # self.page = dict()
        self.create_block(proof = 1, previous_hash = '0', page={"Genesis Block containing list of permissioned hospitals": ['Siemens 1', 'Siemens 2', 'Siemens 3']})
        
  
    def create_block(self, proof, previous_hash, page):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str( datetime.datetime.now()),
                 'proof':  proof,
                 'data': page,
                 'previous_hash': previous_hash
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256( str( new_proof**2 - previous_proof**2 ).encode()).hexdigest()  
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256( str( proof**2 - previous_proof**2).encode()).hexdigest()  
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            return True
    def reciever_self(self, pid, report, prevID, location, flag, dID):
        page = {pid:[prevID, report, location, dID, flag]}
        # previous_block = blockchain.get_previous_block()
        # previous_proof = previous_block['proof']
        # proof =  blockchain.proof_of_work(previous_proof)
        # previous_hash = blockchain.hash(previous_block)
        return page#blockchain.create_block(proof,previous_hash, page)
    
    def get_random_string(self):

    # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        return result_str
    
    def finder(self,tmp1):
        tmp2 = int(tmp1)-1
        responser.append({tmp2+1 : self.chain[tmp2]})
        tmp3 = self.chain[tmp2]['data']['one'][1]
        return tmp3
        #print(tmp3)
        
     
app = Flask(__name__)
 
blockchain = Blockchain()

@app.route('/post_data', methods=['GET'])
def post_data():
    data = request.get_json
    dataa = json.dumps(data)
    dataaa = list(dataa.keys())[0]
    #dataaaa = []
    a = dataaa
    b = dataa[dataaa][0]
    c = dataa[dataaa][1]
    d = dataa[dataaa][2]
    e = dataa[dataaa][3]
    f = dataa[dataaa][4]
    # data.append(a)
    # data.append(b)
    # data.append(c)
    # data.append(d)
    # data.append(e)
    # data.append(f)
    block = receiver(a,b,c,d,e,f)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'] }
    return jsonify(response), 200

@app.route('/mine_block',methods=['GET'])
def mine_block():

    #data = receiver()
    data = request.get_json()
    dataa = json.dumps(data)
    dataaa = list(dataa.keys())[0]
    a = dataaa
    b = dataa[dataaa][0]
    c = dataa[dataaa][1]
    d = dataa[dataaa][2]
    e = dataa[dataaa][3]
    f = dataa[dataaa][4]
    dataaaa = receiver(a,b,c,d,e,f)
    #data = "Hello"
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof =  blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash, data)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'] }
    return jsonify(response), 200

@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length':len(blockchain.chain) }
    return jsonify(response), 200



@app.route('/findData', methods=['POST'])
def findData():
    responser.clear()
    data = request.get_json()
    tmp1 = data['prevID']
    #tmp2 = data['iterator']
    response = blockchain.finder(tmp1)
    for i in range(0, 2):
        response = blockchain.finder(response)
    return jsonify(responser)
    



@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid  = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'All good. The blockchain is valid'}
    else:
        response = {'message':'Houston, we have a problem. The blockchain is not valid'}
    return jsonify(response), 200

@app.route('/testing', methods=['GET'])
def testing():
    data = request.get_json()
    tmp1 = "xyz"#data['pid']
    tmp2 = "xyz"#data['prevID']
    tmp3 = "xyz"#data['report']
    tmp4 = "xyz"#data['location']
    tmp5 = "xyz"#data['flag']
    tmp6 = "xyz"#data['dID']
    tmp7 = blockchain.reciever_self(tmp1,tmp2,tmp3,tmp4,tmp5,tmp6)
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof =  blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash, tmp7)

    #return jsonify(block)
@app.route('/testingten',methods=['GET'])
def testingten():
    for i in range(0,1000):
        testing()
    return "Mines 1000"

@app.route('/testing2', methods=['POST'])
def testing2():
    data = request.get_json()
    tmp1 = data['pid']
    tmp2 = data['prevID']
    tmp3 = data['report']
    tmp4 = data['location']
    tmp5 = data['flag']
    tmp6 = data['dID']
    tmp7 = blockchain.reciever_self(tmp1,tmp2,tmp3,tmp4,tmp5,tmp6)
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof =  blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash, tmp7)

    return jsonify(block)

@app.route('/brute',methods=['POST'])
def brute():
    data = request.get_json()
    tmp1 = data['pid']
    tmpChain = blockchain.chain
    listing = []
    for i in range(0,len(tmpChain)):
        stringer = list(tmpChain[i]['data'].keys())[0]
        if stringer==tmp1:
            listing.append(tmpChain[i])
    return jsonify(listing)
 
app.run(host = '0.0.0.0',port = 5000)