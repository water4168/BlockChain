# coding=UTF-8
from locust import HttpLocust, TaskSet, task
import json


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
    """
    挂单的策略：买单价格限制在1-5， 卖单价格限制10-6；
    在价格限制的范围内，循环挂单，每次0.0001的数量。
    """

    @task(1)
    def entrust_in(self):
        TentrustCount_in = 0.0001
        while TentrustCount_in < float(1):
            TentrustPrice_in = int(0)
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
            TentrustCount_in += 0.0001
            TentrustCount_in=float("%.4f" %TentrustCount_in)


    # 挂单卖出
    @task(1)
    def entrust_out(self):
        TentrustCount_out = 0.0001
        while TentrustCount_out < float(1):
            TentrustPrice_out = int(5)
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
                        print('entrust_in success')
                else:
                    print("price is over")
            TentrustCount_out += 0.0001
            TentrustCount_out=float("%.4f" %TentrustCount_out)



class WebsiteUser(HttpLocust):
    task_set = EntrustTask
    min_wait = 3000
    max_wait = 5000


