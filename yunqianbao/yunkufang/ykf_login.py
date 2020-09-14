from locust import HttpLocust,Locust, TaskSet, task
import time,json,random,sys,queue
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
from test_script.publicscript.publicRequestMethod import PublicRequest




class UserLogin(TaskSet):
    def login(self,header):
        """
        登录
        """
        try:
            userItem = self.locust.queueData.get()  #获取队列里的数据
            # print("登录用户：",userItem)
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        print("shoujihao ====== {}".format(userItem['mobile']))
        
        login_urlName = "登录"
        login_url = "https://test-api.518aic.com/app/user/login"
        login_data = {
                "password": "ren123456",
                "mobile": userItem['mobile'],
            }
        print("userItem['mobile']====",userItem['mobile'])
        with self.client.post(login_url,data = login_data, headers = header,name = login_urlName+login_url,verify = False,allow_redirects=False,catch_response=True,timeout = 30) as response:
            result = json.loads(response.text)
            # result = response.text
            print("result======",result)
            if "status" in result and result["status"] == 200:
                response.success()
            else:
                response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(login_urlName,login_url,login_data,result))
            return result


    