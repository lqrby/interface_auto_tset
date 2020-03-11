from locust import HttpLocust,Locust, TaskSet, task
import time
import random
import queue
import json,sys
sys.path.append("F:/myTestFile/TestObject/YouTime")
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicFunction import PublicFunction
from test_script.wode.woDeQianBao import WoDeQianBao
import decimal
from faker import Faker
from common.pictures import SelectPictures
# from common.publicData import PublicData
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe
from test_script.publicscript.publicFunction import PublicFunction
from test_script.homePage import HomePage
# 定义用户行为
class LiuCheng(TaskSet):
    def on_start(self):
        # fake = Faker("zh_CN")
        # lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
        # lat = lonAndLat[0]
        # lon = lonAndLat[1]
        # LoginAndZhuCe(self).userRegister() #注册
        self.loginUserData = LoginAndZhuCe(self).userLogin() 
        self.loginUser = self.loginUserData["data"]
        print("------------------------------:{}".format(self.loginUser))
        self.loginUser["location"]= {
            "address": '北京市通州区', #fake.company(),
            "lon": 116.63309759819349,
            "lat": 39.90490152753389
        }
        self.header = self.loginUserData['header']

    # @task(1) 
    def guanZhu(self):
        uid = 10001
        userItem = HomePage(self).fuJinDeRen_Detail(self.header,uid) #获取用户详情
        PublicFunction(self).FocusOnly(self.header,userItem)



    '''
    # 附近的人列表》查看人员详情 》点赞 
    '''  
    # @task(1)        
    def fujinderen(self):
        # 获取附近的人列表
        fjdrList_res = HomePage(self).fuJinDeRen_list(self.header)
        fjdrList = fjdrList_res["data"]
        if fjdrList:
            for useritem in random.sample(fjdrList, random.randint(1,len(fjdrList))):
                # 查看的人详情
                userdetail_res = HomePage(self).fuJinDeRen_Detail(self.header,useritem["uid"])
                userdetail = userdetail_res["data"]
                userdetail['id'] = userdetail['uid']
                userdetail['type'] = 2
                # 给人员点赞
                PublicFunction(self).dianZan(self.header, userdetail)
        
    '''
    # 附近的动态列表》查看动态详情 》点赞 
    '''  
    # @task(1)        
    def fujindongtai(self):
        # 获取附近动态列表
        fjdtList_res = HomePage(self).fuJinDongTai_list(self.header,self.loginUser)
        fjdtList = fjdtList_res["data"]
        if fjdtList:
            for dtitem in random.sample(fjdtList, random.randint(1,len(fjdtList))):
                # 查看动态详情
                userdtdetail_res = HomePage(self).fuJinDongTai_Detail(self.header,dtitem)
                userdtdetail = userdtdetail_res["data"]
                userdtdetail['id'] = userdtdetail['did'] 
                userdtdetail['type'] = 0
                # 给动态点赞
                PublicFunction(self).dianZan(self.header, userdtdetail)
                # 发布动态
                HomePage(self).newDynamics(self.header)


    '''
    # 附近的价值列表》查看价值详情 》点赞 》发布价值
    '''  
    # @task(1)        
    def fujinjiaZhi(self):
        # 获取附近价值列表
        fjjzList_res = HomePage(self).fuJinJiaZhi_list(self.header,self.loginUser)
        fjjzList = fjjzList_res["data"]
        if fjjzList:
            for praisedUser in random.sample(fjjzList, random.randint(1,len(fjjzList))):
                # 查看价值详情
                jzdetail_res = HomePage(self).fuJinJiaZhi_Detail(self.header, praisedUser)
                jzdetail = jzdetail_res["data"]
                jzdetail['id'] = jzdetail['wid'] 
                jzdetail['type'] = 0
                # 给价值点赞
                PublicFunction(self).dianZan(self.header, jzdetail)
                #发布价值
                print("uid:{}".format(self.loginUser["uid"]))
                HomePage(self).publishingValue(self.header,self.loginUser["uid"])
        else:
            print("---不好意思没有数据---")

    @task(1)        
    def fujinjiaZhi2(self):
        #发布价值
        print("uid:{}".format(self.loginUser["uid"]))
        HomePage(self).publishingValue(self.header,self.loginUser["uid"])



    '''
    # 我的钱包》去审核 》审核 
    '''  
    # @task(1)        
    def myWallet(self):
        # 去审核
        if self.loginUser["userType"] == 2:
            qushenhe_res = WoDeQianBao(self).quShenHe(self.header)
            i = 1
            while "code" in qushenhe_res and qushenhe_res["code"] == 468:
                qushenhe_res = WoDeQianBao(self).quShenHe(self.header)
                if i>100:
                    # self.interrupt()
                    break
                i += i
            # 审核
            if 'code' in qushenhe_res and qushenhe_res["code"] == 200:
                obj = qushenhe_res["data"]["reviewId"]
                WoDeQianBao(self).shenHe(self.header,obj)
            else:
                print("xxx提交异常或审核超时xxx{}".format(qushenhe_res))
        else:
            print("----该用户没有审核权限---{}".format(self.loginUser))
            self.interrupt()
            

        

class WebsiteUser(HttpLocust):
    task_set = LiuCheng
    min_wait = 600
    max_wait = 1000
    host = "http://192.168.1.30"
    users = queryUsers() #多个用户
    print(queryUsers(),type(queryUsers()))
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   