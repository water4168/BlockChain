# coding=UTF-8
from locust import HttpLocust, TaskSet, task
import json


"""
这是一份交易所挂单脚本，不包含触发撮合的内容

挂单的策略：买单价格限制在1-5， 卖单价格限制6-10；
无论买入卖出，首次循环时委托数量为0.0001，第二次循环为0.0002，以此类推，直到数量等于1才退出整个循环

借助locust组件，每一个用户就是一个协程，每个协程初始化(on_start)后，都在不停地执行买入(entrust_in)和卖出(entrust_out)方法。
"""
class EntrustTask(TaskSet):

    def on_start(self):
        self.in_user = '5daee847-5565-4b9b-afdd-ef9fca69b95d'
        self.out_user = '5daee847-5565-4b9b-afdd-ef9fca69b95d'
        self.url_entrust = 'http://192.168.1.248:9079/api/transaction/api/v1/user/entrust'

        self.header_in = {
            "Accept": "*/*",
            "accessToken": "05406a2b-e597-444e-948d-d141f025770b",
            "currLanguage": "zh",
            "Content-Type": "application/json"
        }
        self.header_out= {
            "Accept": "*/*",
            "accessToken": "21988110-4c56-45a5-a864-68dc4a42462c",
            "currLanguage": "zh",
            "Content-Type": "application/json"
        }


    #挂单买进
    @task(1)
    def entrust_in(self):
        TentrustCount_in = 0.0001 # 买入初始数量
        while TentrustCount_in < float(1):
            TentrustPrice_in = int(0)  # 买入初始价格
            for i in range(5):
                if i < 5:
                    TentrustPrice_in += 1
                    print(TentrustPrice_in, TentrustCount_in)
                    body_data_in = {"entrustPrice":str(TentrustPrice_in), "entrustCount":str(TentrustCount_in), "marketId":"49", "type":"1", "dealPassword":"qwe123"}
                    lkj=json.dumps(body_data_in, separators=(',', ':')) # 为了避免解析失败，转化为json格式时，忽略掉空格/换行符
                    print(lkj)
                    response = self.client.request(
                                        method='POST',
                                        url=self.url_entrust,
                                        data=lkj,
                                        headers=self.header_in
                                        )
                    result = response.json()
                    if result["status"]["msg"] != "成功":
                        print(response.text)
                    else:
                        print('entrust_in success')

                else:
                    print("price is over")
            TentrustCount_in += 0.0001  # 每for循环一次，委托数量+0.0001
            TentrustCount_in=float("%.4f" %TentrustCount_in)


    # 挂单卖出
    @task(1)
    def entrust_out(self):
        TentrustCount_out = 0.0001 # 卖出初始数量
        while TentrustCount_out < float(1):
            TentrustPrice_out = int(5) # 卖出初始价格
            for i in range(5):
                if i < 5:
                    TentrustPrice_out += 1
                    print(TentrustPrice_out, TentrustCount_out)
                    body_data_out = {"entrustPrice": str(TentrustPrice_out), "entrustCount": str(TentrustCount_out), "marketId": "49", "type": "2", "dealPassword": "a123456"}
                    response = self.client.request(
                                        method='POST',
                                        url=self.url_entrust,
                                        data=json.dumps(body_data_out, separators=(',', ':')),
                                        headers=self.header_out
                                        )
                    result = response.json()
                    if result["status"]["msg"] != "成功":
                        print(response.text)
                    else:
                        print('entrust_out success')
                else:
                    print("price is over")
            TentrustCount_out += 0.0001 # 每for循环一次，委托数量+0.0001
            TentrustCount_out=float("%.4f" %TentrustCount_out)



class WebsiteUser(HttpLocust):
    task_set = EntrustTask
    min_wait = 3000
    max_wait = 5000


