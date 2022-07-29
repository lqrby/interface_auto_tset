import random,os,sys,time
file_path = os.path.join(os.path.abspath('.'))
file_path = file_path.replace('\\', '/')
sys.path.append(file_path)
from utils.mysqlServer import MysqlDb
from user_data import userItems

class DependentData():

    def __init__(self):
        self.MysqlDb = MysqlDb()
        '''1.用户列表'''
        user_sql = "select * from ourydc_app_user limit 50" # 获取用户对象1  {"options":{"userId":"user_id"}}
        '''2.聊天室列表'''
        chat_room_sql = "select * from ourydc_app_chat_room where room_state=1"  # 获取聊天室对象2  { "options":{"roomId":"room_id"}}

        '''
        # 3.语音邀请记录列表
        { "options":{"orderId":"order_id"}, "common":{"userId": "to_user_id"}}   
        '''
        invitation_record_sql = """select r.order_id,r.from_user_id,r.to_user_id, r.type,r.state,o.state from ourydc_app_user_voice_chat_order as o,
                ourydc_app_voice_order_invitation_record as r where o.id=r.order_id and o.state <= 2 and r.state = 5 limit 100 """  

        '''
        # 4.关闭订单列表
        {"options":{"roomId":"room_id","orderId":"id"},"common":{"userId": "user_id"}}         
        '''
        order_sql = "select * from ourydc_app_user_voice_chat_order where state <=2 limit 10"  # 主动关闭订单4  {"options":{"roomId":"room_id","orderId":"id"}}

        '''5.动态列表'''
        dynamic_sql = "select * from ourydc_app_user_dynamic order by insdt limit 20"  #{"options":{"dynamicId":"id"}}

        # '''6.关注列表'''
        # follow_sql = "select * from ourydc_app_user_dynamic order by insdt limit 20"

        


        

        self.sqlList =[
            {"id":1,"sql":user_sql}, #用户列表
            {"id":2,"sql":chat_room_sql}, #房间列表
            {"id":3,"sql":invitation_record_sql}, #邀请记录列表
            {"id":4,"sql":order_sql}, #订单列表
            {"id":5,"sql":dynamic_sql}, #动态列表
            {"id":7,"sql":self.my_follow()}, #动态列表
            
        ]

    '''7.我的动态列表'''
    def my_follow(self):
        userItem = random.choice(userItems)
        my_dynamic_sql = "select * from ourydc_app_user_dynamic where user_id='{}' order by insdt limit 20".format(userItem.get("user_id"))
        return my_dynamic_sql
    #查询当前开播的聊天室
    def getData(self,num):
        if num == 99:
           return self.getTime()
        queryList = []
        for item in self.sqlList:
            if item["id"] == num:
                queryList = self.MysqlDb.query(item["sql"])
        if len(queryList) > 0:
            return random.choice(queryList)
        else:
            return 0

    """时间戳id 99 { "options":{"userLocalTimestamp":"userLocalTimestamp"}}"""
    def getTime(self):
        userLocalTimestamp = {"userLocalTimestamp":str(int(time.time()*1000))}
        return userLocalTimestamp

    

if __name__ == "__main__":
    res = DependentData().getData(5)
    print(res)

