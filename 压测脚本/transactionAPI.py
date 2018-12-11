import json
import random
from random import choice
import bitcoin
from ecpy.ecdsa import ECDSA
from ecpy.curves import Curve
from ecpy.keys import ECPrivateKey
from Crypto.Hash.SHA256 import SHA256Hash
from locust import HttpLocust,TaskSet,task


'''
BTC、ETH这些公链一般提供RPC接口让我们向网络发起交易请求！
直接用压测工具压测RPC的方法，还没有实验过。
locust默认针对HTTP的，而且ETH封装好的HTTP接口很多，只要构造好相应参数，就能用locust发起压测！

所以压测公链，先弄清楚交易请求的参数是怎么生成的，然后找轮子实现即可！

'''
S = set()
setLength = 0
# 字节类型转十六进制字符串
def ByteToHex(bins):
    return ''.join([ "%02X" % x for x in bins ]).strip()


# 字符串转十六进制
def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])


# 这个获取nonce的方法，待优化
def getNonce():
    ranNonce = choice(range(1,599999999))
    nonce = str(ranNonce)
    #print(nonce)
    if nonce not in S:
        return nonce
    else:
        getNonce()

# 从含有1000个地址的json文件取出list对象
jsondata = open("./walletlist.json", encoding='utf-8')
strJson = json.load(jsondata) # 返回list类型({},{},{}····)


def getRanFromAddress():
    fromList = strJson[0:501]
    ranOne = choice(fromList)
    return  ranOne["address"], ranOne["publickey"], ranOne["privateKey"]


def getRanToAddress():
    toList = strJson[501:1001]
    ranOne = choice(toList)  # return random dict
    return ranOne["address"]


def createPriKey(wifKey):
    wif_encoding_private_key = wifKey
    wifUNCompressed = bitcoin.decode_privkey(wif_encoding_private_key, 'wif_compressed')
    decimalToHex = bitcoin.encode(wifUNCompressed, 16) # return str
    cv = Curve.get_curve('secp256k1')
    pv_key = ECPrivateKey(int("0x"+decimalToHex, 16), cv) # 16进制str 转为 int
    return pv_key


def getSignData(original_data,pk):

    json_str = json.dumps(original_data).replace(' ', '')
    byte_str = json_str.encode()
    sha256 = SHA256Hash(byte_str)
    byte_str_hash = sha256.digest()  # 返回byte类型哈希
    # 私钥签名
    signer = ECDSA()
    raw_sig = signer.sign(byte_str_hash, pk)  # sign返回的byte对象
    hex_sig = ByteToHex(raw_sig).lower()  # 将签名后byte转为hex,并修改字母为小写
    return hex_sig


# 上面全部的方法，都是为了这个服务的。
def makeRawData():
    global setLength
    nonceValue = getNonce()
    fromAddress, pubkey, prikey = getRanFromAddress()
    toAddress = getRanToAddress()
    original_data = {"tokenID":"803a8330f2b911e8a4dee7f774b57dcc",
                     "fromAddress":fromAddress,
                     "toAddress":toAddress,
                     "number":"0.00001",
                     "nonce":nonceValue,
                     "pubKey":pubkey}

    S.add(original_data["nonce"]) # 用过的nonce值放进集合
    setLength += 1
    pk = createPriKey(prikey)
    hex_sig = getSignData(original_data, pk)
    sendData = {"origin": original_data, "signature": hex_sig}
    json_sendData_str = json.dumps(sendData).replace(' ', '')  # 去掉空格
    hex_sendData = json_sendData_str.encode("utf-8").hex()
    return hex_sendData


class UdoTransfer(TaskSet):
    global setLength

    def setup(self):
        pass

    def teardown(self):
        print("一共发出了 %d 笔交易请求！"%setLength)
        S.clear()  # 清空集合

    @task(1)
    def manyTomanyTransfer(self):
 
        toUrl = "http://youhost/v1/wallet/sendRawTransaction"
        sendRawData = {"rawData": "%s" % makeRawData()}

        response = self.client.request(method="POST", url=toUrl, data=sendRawData)

        result = response.json()
        if result["status"] == True:
            print("转账成功")
            #pass
        else:
            print(result)



class WebsiteUser(HttpLocust):
    task_set = UdoTransfer
    min_wait = 1000
    max_wait = 3000
