from locust import HttpLocust,Locust, TaskSet, task
import time,json,random,sys,queue

sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
from Interface.QueryUsers import queryUsers_ykf
from test_script.publicscript.publicRequestMethod import PublicRequest
from yunkufang.ykf_login import UserLogin
from yunkufang.chuangXinShiChang import ChuangXinShiChang


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() 

events.hatch_complete += on_hatch_complete  #挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class CXSCLiuCheng(TaskSet):

   
    def on_start(self):
        self.header = {
            "User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; ALP-TL00 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36 YunKuFang/1.3.3",
            "mobile-system":"android8.0.0",
            "app-type":"Android",
            "app-version":"1.3.3",
            "app-version-code":"13",
            "mobile-unid":"866215038845167",
            "mobile-type":"ALP-TL00",
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection":"Keep-Alive"
        }
        self.loginRes = UserLogin(self).login(self.header)
        self.token = self.loginRes['data']['token']
        print("登录成功----",self.loginRes)
        print("token----",self.token)
        self.cxscClassObj = ChuangXinShiChang(self)
        all_locusts_spawned.wait() #在此设置了集合点

    @task
    def liuCheng(self):
        cxsc_list = self.cxscClassObj.cxsc_list(self.token,self.header)  #创新市场列表
        if cxsc_list:
            cxsc_detail = self.cxscClassObj.cxsc_detail(cxsc_list,self.token,self.header) #创新市场项目详情
            if cxsc_detail:
                ququerenOBJ = self.cxscClassObj.quRenGou(cxsc_detail,self.token,self.header) #创新市场去认购
                if ququerenOBJ:
                    rengou = self.cxscClassObj.renGou(ququerenOBJ,cxsc_detail['data']['id'],self.token,self.header)
                    if not rengou:
                        print("认购出现问题XXXX========{}".format(rengou))
                else:
                    print("创新市场去认购出现问题XXXX==========".format(ququerenOBJ))
            else:
                print("创新市场列详情出现问题XXXX")
        else:
            print("创新市场列表出现问题XXXX")
    


class WebsiteUser(HttpLocust):

    task_set = CXSCLiuCheng
    min_wait = 100
    max_wait = 300
    # host = "https://test-api.iyunkf.com/"
    host = "None"
    # users = queryUsers_ykf(100,100) #多个用户
    # print("users======",users)
    users = []
    for u in range(15000000000,15000001001):
        users.append({'mobile': u})
    
    # print(users)
    # users = [
    #     {'password': 'ren123456', 'mobile': '15001200238'},
    #     {'password': 'ren123456', 'mobile': '18810798467'},
    #     {'password': 'ren123456', 'mobile': '15000000545'},
    #     {'password': 'ren123456', 'mobile': '15000000546'},
    #     {'password': 'ren123456', 'mobile': '15000000547'},
    #     {'password': 'ren123456', 'mobile': '15000000548'},
    #     {'password': 'ren123456', 'mobile': '15000000551'},
    #     {'password': 'ren123456', 'mobile': '15000000550'},
    #     {'password': 'a123456789', 'mobile': '18246463219'},
    #     {'password': 'a123456789', 'mobile': '13314627183'},
    #     {'password': 'a123456789', 'mobile': '18704651002'},
    #     {'password': 'a123456789', 'mobile': '17600920288'},
    #     {'password': 'a123456789', 'mobile': '18410301111'},
    #     {'password': 'a123456789', 'mobile': '18410301112'},
    #     {'password': 'a123456789', 'mobile': '18410301113'},

    #     ] #单个用户
    queueData = queue.Queue()
    for user in users:
        queueData.put_nowait(user)   

    def setup(self):
        print('locust setup')
 
    