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

# class YunQianBaoMan(TaskSet):
#     def on_start(self):
#         self.header ={
#             "Connection":"keep-alive",
#             "app-type":"android", #android
#             "mobile-unid":"866215038845167",
#             "app-version":"5.4.91",
#             "mobile-type":"HUAWEIALP-TL00(8.0.0)",
#             "mobile-system":"android8.0.0",
#             "device-tokens": "",  #AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN
#             "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
#             "Content-Type":	"application/x-www-form-urlencoded",
#         }
#         self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"

#     # @task
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
#         LoginAndZhuCe(self).zhuCe(url,zc_data,self.header)

#     @task
#     def loginUser(self):
#         """"
#         登录》获取首页》判断密保(未设置密保先设置密保)》判断是否实名(未实名则先实名)
        
#         """
#         try:
#             mobile = self.locust.queueData.get()  #获取队列里的数据
#             # print("登录用户：",userItem)
#         except queue.Empty:                     #队列取空后，直接退出
#             print('no data exist')
#             exit(0)
#         password = "defe12aad396f90e6b179c239de260d4"
#         device_tokens = "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN"
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
#         login_res = LoginAndZhuCe(self).login(url,login_data,self.header)

#         # 获取首页的参数
#         if login_res:
#             index_url = "v2/my/index"
#             index_data ={
#                 "access_token":login_res["access_token"],
#                 "sign":"",
#                 "timestamp":str(int(time.time()))
#             }

#             # 获取首页
#             index_data["sign"] = GetDataSign().sign_body(index_url,index_data, self.apikey)
#             index_res = LoginAndZhuCe(self).login(index_url,index_data,self.header)
#             print("获取首页返回值==={}".format(index_res))
#             # 判断是否已设置密保
#             if index_res["is_safe"] == "0":
#                 # print("未设置密保=======================")
#                 answer = '["beijing","tianjin","shanghai"]'
#                 # answer = ["".join(i) for i in answer.items() if i[1] and i[0] != "sign"]
#                 base64_encrypt = base64.b64encode(answer.encode('utf-8'))
#                 # print("密保答案====={}".format(base64_encrypt))
#                 mibao_url = "v2/safe/set-safe-issue"
#                 mibao_data = {
#                     "access_token":login_res["access_token"],
#                     "answer":"W3siYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMCIsImlzc3VlIjoiMSJ9LHsiYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMCIsImlzc3VlIjoiMyJ9LHsiYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMSIsImlzc3VlIjoi5YyX5LqsIn1d",
#                     "timestamp":str(int(time.time())),
#                     "sign":""
#                 }
#                 # print("mibao_data===={}".format(mibao_data))
#                 # 提交设置的密保
#                 mibao_data["sign"] = GetDataSign().sign_body(mibao_url,mibao_data, self.apikey)
#                 LoginAndZhuCe(self).login(mibao_url,mibao_data,self.header)

#             # 判断是否实名(未实名则先实名)
#             if login_res["info"]["idcard"] != True:
#                 path = "F:/myTestFile/TestObject/YouTime/yunqianbao/shenfenzheng.txt"
#                 card = WriteAndReadTextFile().readOneLine_txt(path)
#                 # print("zhengjianhao===={}=={}".format(card,type(card)))
#                 card_list = card.split(" ")
#                 shiming_url = "v2/card/user-real-name"
#                 sm_data = {
#                     "access_token":login_res["access_token"],
#                     "idcard":card_list[1], #身份证号码
#                     "degree":"0",
#                     "sign":"",
#                     "realname":card_list[0], #用户姓名
#                     "timestamp":str(int(time.time())),
#                     "image_face":('tp1.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp1.jpg", "rb"),"image/jpg"), #脸部照片
#                     "image_con":('tp2.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp2.jpg", "rb"),"image/jpg"), #背面照片
#                     "image_hand":('tp3.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp3.jpg", "rb"),"image/jpg") #手持正面照片 
#                 }
#                 # sm_data = {
#                 #     "access_token":login_res["access_token"],
#                 #     "idcard":card_list[1], #身份证号码
#                 #     "degree":"0",
#                 #     "sign":"",
#                 #     "realname":card_list[0], #用户姓名
#                 #     "timestamp":str(int(time.time()))
#                 # }
#                 # files={
#                 #     "file1": ("tp1.jpg", open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp1.jpg", "rb"), "image/jpg"),
#                 #     "file2": ("tp2.jpg", open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp2.jpg", "rb"), "image/jpg"),
#                 #     "file3": ("tp3.jpg", open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp3.jpg", "rb"), "image/jpg")
#                 #     }
#                 # print("m.fileds====================================================={}".format(m.fields))
                
#                 # f ={ "file": (file, open("./images/"+file, "rb"), "image/jpeg")}
#                 # # 实名
#                 sign = GetDataSign().sign_body(shiming_url,sm_data, self.apikey)
#                 # print("sign====================={}".format(sign))
#                 # m.fields["sign"] = sign
#                 # self.header['Content-Type'] = m.content_type
#                 print("m.fields====================={}".format(sm_data))
#                 # self.header['Content-Type'] = m.content_type
#                 # print("m=====m.fields================{}".format(m.fields))

#                 shiming_res = LoginAndZhuCe(self).login(shiming_url,sm_data,self.header)
#                 # print("实名返回值==={}".format(shiming_res))

    


                
    
    


    
# class WebsiteUser(HttpLocust):
#     task_set = YunQianBaoMan
#     min_wait = 600
#     max_wait = 1000
#     host = "https://tyqbapi.bankft.com/"
#     # host = "http://dev.api.bankft.com"
    
#     # users = queryUsers() #多个用户
#     users = []
#     for i in range(18810798215,18810798216):
#         users.append(i)
#     queueData = queue.Queue()
#     for userItem in users:
#         queueData.put_nowait(userItem)   

