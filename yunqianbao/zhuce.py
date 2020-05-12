# from locust import HttpLocust,Locust, TaskSet, task, seq_task
# import random,time,json
# import sys
# sys.path.append("F:/myTestFile/TestObject/YouTime")
# from yunqianbao.qianMing import GetDataSign
# class ZhuCe(TaskSet):
#     def on_start(self):
#         self.header ={
#             "Connection":"keep-alive",
#             "app-type":"android", #android
#             "mobile-unid":"866215038845167",
#             "app-version":"5.4.91",
#             "mobile-type":"HUAWEIALP-TL00(8.0.0)",
#             "mobile-system":"android8.0.0",
#             "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",
#             "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
#             "Content-Type":	"application/x-www-form-urlencoded",
#         }

#     @task   
#     def zhuCe(self):
#         # login_data={
#         #     "password":	"defe12aad396f90e6b179c239de260d4",
#         #     "sms_code":	"123456",
#         #     "mobile":"18810798208",
#         #     "device_tokens":"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",
#         #     "timestamp" : str(int(time.time())),
#         #     "sign":	""
#         # }
#         login_data = {
#             "password":"defe12aad396f90e6b179c239de260d4",
#             "latitude":"39.905662",
#             "mobile":"18810798467",
#             "long":"116.64063",
#             "device_tokens":"",
#             "timestamp":str(int(time.time())),
#             "sign":	"" 
#         }


#         url = "v2/login/login-new"#"v2/login/signup"
#         apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
#         sign = GetDataSign().sign_body(login_data, url, apikey)
#         login_data["sign"] = sign
#         # print("login_data==={}".format(login_data))
#         with self.client.post("/v2/login/login-new", data = login_data, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
#                 zc_res = json.loads(response.text)
#                 # print("结果===={}".format(zc_res))
#                 if 'status' in zc_res and zc_res["status"] == 200:
#                     time.sleep(random.randint(1,3))
#                     response.success()
#                     # response.quitting()
#                     return zc_res["data"]
#                 else:
#                     response.failure("注册报错{}".format(zc_res))
#                     # response.quitting()
#                     # self.interrupt()




# # class WebsiteUser(HttpLocust):
# #     task_set = ZhuCe
# #     min_wait = 600
# #     max_wait = 1000
# #     host = "https://tyqbapi.bankft.com"
#     # host = "http://dev.api.bankft.com"

#     # users = queryUsers() #多个用户
#     # queueData = queue.Queue()
#     # for userItem in users:
#     #     queueData.put_nowait(userItem)   
