# from locust import HttpLocust,Locust, TaskSet, task, seq_task
# import random,time,json
# import base64
# import sys
# import queue
# # from requests_toolbelt import MultipartEncoder
# from requests_toolbelt import MultipartEncoder
# sys.path.append("F:/myTestFile/TestObject/YouTime")
# from yunqianbao.qianMing import GetDataSign
# from yunqianbao.loginAndzhuCe import LoginAndZhuCe
# from common.writeAndReadText import WriteAndReadTextFile
# from yunqianbao.publicRequestMethod import PublicRequest



# class YunQianBaoMan(TaskSet):
#     def on_start(self):
#         self.header ={
#             "Connection":"keep-alive",
#             "app-type":"android", #android
#             "mobile-unid":str(int(round(time.time() * 100000))),
#             "app-version":"5.4.91",
#             "mobile-type":"HUAWEIALP-TL00(8.0.0)",
#             "mobile-system":"android8.0.0",
#             "device-tokens": "",  #AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN
#             "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
#             "Content-Type":	"application/x-www-form-urlencoded",
#         }
#         self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
#         self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
#         self.userData_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"

#     @task
#     def zhuceUser(self):
#         try:
#             mobile = self.locust.queueData.get()  #获取队列里的数据
#             # print("登录用户：",userItem)
#         except queue.Empty:                     #队列取空后，直接退出
#             print('no data exist')
#             exit(0)
#         zc_data = {
#             "password":"defe12aad396f90e6b179c239de260d4",
#             "latitude":"39.905662",
#             "mobile":str(mobile),
#             "long":"116.64063",
#             "device_tokens":"",
#             "timestamp":str(int(time.time())),
#             "sign":	"" 
#         }

#         url = "v2/login/signup"
#         sign = GetDataSign().sign_body(url,zc_data, self.apikey)
#         zc_data["sign"] = sign
#         PublicRequest(self).requestMethod(url,zc_data,self.header)

#     # @task
#     def loginUser(self):
#         """"
#         登录
        
#         """
#         try:
#             mobile = self.locust.queueData.get()  #获取队列里的数据
#             # print("登录用户：",userItem)
#         except queue.Empty:                     #队列取空后，直接退出
#             print('no data exist')
#             exit(0)
#         password = "defe12aad396f90e6b179c239de260d4" #"e10adc3949ba59abbe56e057f20f883e" #
#         device_tokens = "" #"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN"
#         login_data = {
#             "password":password,
#             "latitude":"39.905662",
#             "mobile":str(mobile),
#             "long":"116.64063",
#             "device_tokens":device_tokens,
#             "timestamp":str(int(time.time())),
#             "sign":	"" 
#         }
#         url = "v2/login/login-new"
#         sign = GetDataSign().sign_body(url,login_data, self.apikey)
#         login_data["sign"] = sign
#         #登录
#         login_res = PublicRequest(self).requestMethod(url,login_data,self.header)
#         WriteAndReadTextFile().test_write_txt(self.userData_path,str(login_res))
#         print("================OK==============")

    
# class WebsiteUser(HttpLocust):
#     task_set = YunQianBaoMan
#     min_wait = 600
#     max_wait = 1000
#     host = "https://tyqbapi.bankft.com/"
#     # host = "http://dev.api.bankft.com/"
    
#     # users = queryUsers() #多个用户
#     users = []
#     for i in range(18810798251,18810798300):
#         users.append(i)
#     queueData = queue.Queue()
#     for userItem in users:
#         queueData.put_nowait(userItem)   

