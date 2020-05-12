from locust import HttpLocust,Locust, TaskSet, task, seq_task
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("F:/myTestFile/TestObject/YouTime")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile
from yunqianbao.single.huoQuRenWu import ComTasks
from yunqianbao.single.publicData import PublicDataClass
from yunqianbao.single.userMobile import user_mobile

class YunQianBaoMan(TaskSet):
    def on_start(self):
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":str(int(round(time.time() * 100000))),
            "app-version":"5.4.91",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "",  #AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded",
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        
    # @task
    def userShiMing(self,mobile):
        """
            1.登录
            2.首页
            3.实名
            4.实名状态

        """
        self.publicData = PublicDataClass(self)
        self.login_res = self.zhuCeAndlogin(self.apikey,self.header,mobile)  #登录
        is_safe = self.publicData.index(self.apikey,self.header,self.login_res)  #获取首页
        self.publicData.setMiBao(self.apikey, self.header,self.login_res,is_safe) # 设置密保
        taskdata = self.publicData.getUserType(self.apikey,self.header,self.login_res) #查看实名状态/获取任务
        if taskdata["type"] == 5:
            print("用户状态5====={}".format(taskdata["type"]))
            pass
        elif taskdata["type"] == 3:
            print("用户状态3====={}".format(taskdata["type"]))
            print("{}==需要去后台审核通过实名认证".format(self.login_res))
        elif taskdata["type"] == 1:
            print("用户状态1====={}".format(taskdata["type"]))
            self.publicData.shiMing(self.apikey,self.header,self.login_res,self.sfz_path) #实名认证
        else:
            print("用户状态?====={}".format(taskdata["type"]))
            self.publicData.userLogout(self.apikey,self.header,self.login_res)
    


    # @task(1)   
    # def userlogin(self):
    #     PublicDataClass(self).login(self.apikey,self.header)



    @task(1)   
    def zhuCeUser(self):
        userdata = PublicDataClass(self).zhuceUser(self.apikey,self.header)
        if userdata:
            self.userShiMing(userdata["mobile"])





    # @task
    def zhuCeAndlogin(self,apikey,header,mobile):
        """"
        登录
        
        """
        password = "defe12aad396f90e6b179c239de260d4" #"e10adc3949ba59abbe56e057f20f883e" #
        device_tokens = "" #"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN"
        login_data = {
            "password":password,
            "latitude":"39.905662",
            "mobile":str(mobile),
            "long":"116.64063",
            "device_tokens":device_tokens,
            "timestamp":str(int(time.time())),
            "sign":	"" 
        }
        url = "v2/login/login-new"
        sign = GetDataSign().sign_body(url,login_data, apikey)
        login_data["sign"] = sign
        
        #登录
        loginres = PublicRequest(self).requestMethod(url,login_data,header)
        loginresult = json.loads(loginres.text)
        if 'status' in loginresult and loginresult["status"] == 200 or 'status' in loginresult and loginresult["status"] == "200":
            time.sleep(random.randint(1,3))
            login_res = loginresult["data"]
            loginres.success()
            return login_res
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(url,login_data,loginresult))
            loginres.failure("报错url==={} ，参数==={} ，报错原因==={}".format(url,login_data,loginresult))

    
    


class WebsiteUser(HttpLocust):
    task_set = YunQianBaoMan
    min_wait = 600
    max_wait = 1000
    host = "https://tyqbapi.bankft.com/"
    # host = "http://dev.api.bankft.com/"
    
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   


    

