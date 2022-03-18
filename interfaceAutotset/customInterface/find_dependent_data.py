import random,os,sys
file_path = os.path.join(os.path.abspath('.'))
file_path = file_path.replace('\\', '/')
sys.path.append(file_path)
from utils.mysqlServer import MysqlDb

class DependentData():

    def __init__(self):
        self.MysqlDb = MysqlDb()
        self.sql_one = "select * from ourydc_app_user limit 50" # 随机获取一个用户对象
        self.sql_two = "select * from ourydc_app_chat_room where room_state=1"  # 随机获取一个聊天室对象
        self.sqlList = [self.sql_one,self.sql_two]
           
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