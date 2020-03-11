from locust import HttpLocust,Locust, TaskSet, task
import time,json,random
import queue
from requests_toolbelt import MultipartEncoder
import sys
sys.path.append("F:/myTestFile/TestObject/YouTime")
from test_script.publicscript.publicRequestMethod import PublicRequest
from Interface.Captcha import returnCaptcha




class LoginAndZhuCe(TaskSet):

    def ZhuCeMa(self):
        """
        # 注册码
        """
        # 将verify 设置为 False，Requests 将忽略对 SSL 证书的验证
        header = {"Connection":"keep-alive"}
        zcm_urlName = "注册码"
        zcm_url = "/gateway/member/macregister"
        zcm_data = {
            "qudao": "1",
            "gid": int(time.time()), #设备唯一标识
            "clientid": "e34f1fa5127db91fdda825528c57c9ad8",
            "os": "9",
            "machine": "V1829A",
            "version": "1.0",
            "platform": "android"
        }
        zcm_response = PublicRequest(self).requestMethod(zcm_url,zcm_urlName,zcm_data,header)
        if zcm_response.status_code == 200:
            zcm_res = json.loads(zcm_response.text)
            token = zcm_res['data']['token']
            num = int(time.time())
            self.header = {
                "token":token,
                "time":str(num),
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent":"okhttp/2.7.5",
                "Connection": "keep-alive",
                "Accept-Encoding":"gzip",
                "Host":"192.168.1.30"
            }
            zcm_response.success()
        else:
            print("XXX生成注册码失败XXX===={}".format(zcm_response.status_code))
            zcm_response.failure("XXX生成注册码失败XXX===={}".format(zcm_response.status_code))



    
    def findCaptcha(self,mobile,header):
        '''
        发送短信验证码
        '''
        captcha_urlName = "获取短信验证码"
        captcha_url = "/gateway/member/smscode"
        captcha_data = {
            "mobile": str(mobile),
            "type": 0
        }
        return PublicRequest(self).publicRequest(captcha_url,captcha_urlName,captcha_data,header)  
        



    def userRegister(self):
        """
            注册
        """
        self.ZhuCeMa()
        try:
            # mobile = self.locust.queueMobile.get()  #获取队列里的数据
            mobile = "15188371841"  #获取队列里的数据
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        if self.findCaptcha(mobile,self.header):
            i = 0
            time.sleep(5)
            code = returnCaptcha(self.header["token"])
            while (code == False):
                time.sleep(random.randint(1,5))
                code = returnCaptcha(self.header["token"])
                print("第一次没获取到，再次获取的验证码是：{}".format(code))
                i += 1
                if i>4:
                    print("4444")
                    print("丫的没发送短信验证码")
                    code = "1234"
                    break
        registerData = {
            "password": "c80d171b81624145618791d99107554a",
            "code": str(code),
            "gid": "866215038845167", #str(int(round(time.time() * 100000)))
            "mobile": str(mobile),
            "type":2,
            "resource":1
        }
        registerUrl = "/gateway/member/mobileregister"
        registerUrlName = "注册"
        '''将verify 设置为 False，Requests 将忽略对 SSL 证书的验证   ,
        allow_redirects=False  禁止重定向,
        timeout = 20   超时
        catch_response=True    自定义成功失败
        '''
        registerResponse = PublicRequest(self).requestMethod(registerUrl,registerUrlName,registerData,self.header)  
        register_res = json.loads(registerResponse.text)
        if 'code' in register_res and register_res["code"] == 200:
            registerResponse.success()
        elif 'code' in register_res and register_res["code"] == 438:
            print("手机号{}已存在".format(mobile))
            registerResponse.failure("手机号{}已存在".format(mobile))
        elif 'code' in register_res and register_res["code"] == 437:
            print("验证码失效,请从新发送=====手机号是：{}短信验证码是------{}".format(mobile,code))
            registerResponse.failure("验证码失效,请从新发送=====手机号是：{}短信验证码是------{}".format(mobile,code))
        else:
            print("手机号{}注册失败{}".format(str(mobile),register_res))
            registerResponse.failure("手机号{}注册失败{}".format(str(mobile),register_res))


    # @task(1)   
    def userLogin(self):
        """
        登录
        """
        self.ZhuCeMa()
        try:
            userItem = self.locust.queueData.get()  #获取队列里的数据
            # print("登录用户：",userItem)
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        print("shoujihao ====== {}".format(userItem['mobile']))
        login_urlName = "登录"
        login_url = "/gateway/member/login"
        login_data = {
                "gid": "866215038845167",
                "code": "1234",
                "logintype": 0,
                "mobile": userItem['mobile'],
                "pass": "c80d171b81624145618791d99107554a",
                "channel": 2
            }
        self.loginRes = PublicRequest(self).publicRequest(login_url, login_urlName, login_data, self.header)
        if self.loginRes:
            self.header["token"] = self.loginRes["data"]["token"]
            self.loginRes['header'] = self.header
            '''
            判断用户初始化信息是否完善，不完善则先完善
            '''
            if self.loginRes["data"]['status'] == 0:
                self.initializeUser(self.loginRes["data"],self.header)
            return self.loginRes


    def initializeUser(self,loginUser,header):
        '''
        初始化用户信息
        '''
        sex = random.randint(1,2)
        nickname = u'遍地开花'+str(loginUser['uid'])
        year = random.randint(1919,2007)
        month = random.randint(1,12)
        day = ''
        if month == 2:
            day = random.randint(1,28) 
        else:
            day = random.randint(1,30)
        strmonth = self.zhuanHuan(month)
        strdat = self.zhuanHuan(day)
        birthday = str(year)+strmonth+strdat
        tp1 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/97dc4501edd919ef819631cf00e6ea63.png"
        tp2 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp3 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/3f37c38a04423e67f811902d901d0a63.png?rnd=0"
        tp4 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp5 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp6 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp7 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp8 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp9 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        picture = [tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9]
        avatar = random.choice(picture)
        cs_data = {
            "sex": sex,
            "nickname": nickname,
            "birth": birthday,
            "avatar": avatar
        }
        cs_url = "/gateway/member/editinfo"
        cs_urlName = "初始化用户信息"
        return PublicRequest(self).publicRequest(cs_url, cs_urlName, cs_data, header)


    def zhuanHuan(self,number):
        if number>9:
            return str(number)
        else:
            return "0"+str(number)
            

    
    


