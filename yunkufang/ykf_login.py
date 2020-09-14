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
        login_urlName = "登录"
        login_url = "https://test-api.518aic.com/app/user/login"
        login_data = {
                "password": "ren123456",
                "mobile": userItem['mobile'],
            }
        with self.client.post(login_url,data = login_data, headers = header,name = login_urlName+login_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "status" in response.text:
                result = json.loads(response.text)
                if "status" in result and result["status"] == 200:
                    response.success()
                    return result
                else:
                    response.failure("登录报错url==={}-{} ，登录报错原因==={}{}".format(login_urlName,login_url,response,response.text))
            else:
                response.failure("登录严重失败报错url==={}-{} ，登录严重失败报错原因==={}{}".format(login_urlName,login_url,response,response.text))


    