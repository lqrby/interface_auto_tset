from locust import HttpLocust,Locust, TaskSet, task
import time,json,random,sys
sys.path.append("F:/myTestFile/TestObject/YouTime")
from test_script.publicscript.publicRequestMethod import PublicRequest






# 我的钱包
class WoDeQianBao(TaskSet):
    '''
    # 去审核  
    '''        
    # @task(1)  
    def quShenHe(self,header):
        qsh_url = "/gateway/member/openReview"
        qsh_urlName = "去审核"
        qsh_res = PublicRequest(self).requestMethod(qsh_url, qsh_urlName, {}, header)
        return json.loads(qsh_res.text)
        
    '''
    # 审核  
    '''                
    def shenHe(self,header,reviewId):
        time.sleep(random.uniform(10,20))
        num = random.choice(["111","000","111","111","111","011","111","100","111","111","101","111","010","111"])
        sh_data = {
            "reviewResult": num,
            "reviewId": reviewId
        }
        sh_url = "/gateway/member/openReview"
        sh_urlName = "审核"
        shenHe_res =  PublicRequest(self).publicRequest(sh_url, sh_urlName, sh_data, header)
        if shenHe_res:
            print("审核完毕，坐等奖励！！！")
            time.sleep(random.uniform(0.1,1)) 
        
        

    '''
    # 账单列表
    '''  
    # @task(1) 
    def zhangDan_list(self,header):
        #账单列表
        zdList_ata = {
            "page": 1,
            "type": 0,
            "limit": 20
        }
        zdList_url = "/gateway/member/bill"
        zdList_urlName = "账单列表"
        return PublicRequest(self).publicRequest(zdList_url, zdList_urlName, zdList_ata, header)


    '''
    # 兑换原始股
    '''  
    # @task(1) 
    def duiHuan(self,header):
        #账单列表
        dhysg_url = "/gateway/member/accountinfo"
        dhysg_urlName = "兑换原始股"
        PublicRequest(self).publicRequest(dhysg_url, dhysg_urlName, {}, header)
        
            