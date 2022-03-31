import random,os,sys
file_path = os.path.join(os.path.abspath('.'))
file_path = file_path.replace('\\', '/')
sys.path.append(file_path)
from utils.mysqlServer import MysqlDb

class DependentData():

    def __init__(self):
        self.MysqlDb = MysqlDb()
        self.app_user_sql = "select * from ourydc_app_user limit 50" # 获取用户对象1
        self.chat_room_sql = "select * from ourydc_app_chat_room where room_state=1"  # 获取聊天室对象2  { "options":{"roomId":"room_id"}}
        '''
        # 语音邀请记录id 3
        { "options":{"orderId":"order_id"}, "common":{"userId": "to_user_id"}}   
        '''
        self.invitation_record_sql = """select r.order_id,r.from_user_id,r.to_user_id, r.type,r.state,o.state from ourydc_app_user_voice_chat_order as o,
                ourydc_app_voice_order_invitation_record as r where o.id=r.order_id and o.state <= 2 and r.state = 5 limit 100 """  
        '''
        # 主动关闭订单id 4
        {"options":{"roomId":"room_id","orderId":"id"},"common":{"userId": "user_id"}}         
        '''
        self.close_order_sql = "select * from ourydc_app_user_voice_chat_order where state <=2 limit 10"  # 主动关闭订单4  {"roomId":"room_id"}
        self.sqlList = [self.app_user_sql,self.chat_room_sql,self.invitation_record_sql,self.close_order_sql]
           
    #查询当前开播的聊天室
    def getData(self,num):
        charroomList = self.MysqlDb.query(self.sqlList[num-1])
        if len(charroomList) > 0:
            return random.choice(charroomList)
        else:
            return 0

    # def get_users(self):
    #     sql = "select * from ourydc_app_user limit 50"
    #     userList = self.MysqlDb.query(sql)
    #     if len(userList) > 0:
    #         return random.choice(userList)
    #     else:
    #         return 0

if __name__ == "__main__":
    res = DependentData().find_launch_chat_room()
    print(res)

