'''
Author: your name
Date: 2021-09-23 18:27:44
LastEditTime: 2021-10-22 17:50:38
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /lk_pressure/utils/db_util.py
'''
import sys, pymysql, datetime,json
from warnings import filterwarnings

filterwarnings("ignore",category=pymysql.Warning)

class MysqlDbUtil:
    def __init__(self):
        #建立数据库连接
        self.conn = pymysql.connect(host='8.131.233.25',port=3306,user='liuyang',password='lY@6083',db='autotest',charset='utf8')
        # self.conn = pymysql.connect(host='localhost',port=3306,user='root',password='ren123456',db='autotest',charset='utf8mb4')
        self.cursors = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        #关闭游标
        self.cursors.close()
        #关闭连接
        self.conn.close()

    def query(self, sql, state="all"):
        """
        查询
        """
        self.cursors.execute(sql)
        # data = {}
        if state == "all":
            data = self.cursors.fetchall()
        else:
            data = self.cursors.fetchone()
        return data


    def execute(self, sql):
        """
        更新、修改、删除
        """
        try:
            print("sql=======",sql)
            #使用execute操作sql
            rows = self.cursors.execute(sql)
            #提交事务
            self.conn.commit()
            return rows
        except Exception as e:
            print("数据库操作异常:{}".format(e))
            #事务回滚修改
            self.conn.rollback() 
        

if __name__ == "__main__":
    # r = MysqlDb().query("select * from `case`"
    # sql = "INSERT INTO `case` (app,module,run) VALUES('youtime','user','yes');"
    # sql = "select room_id from ourydc_app_chat_room where identity_id='1001032'"  #查询房间id
    # sql = "select room_id from ourydc_app_chat_room where room_manager = '0002021092815305052200'"
    sql = "select * from apitest_case"
    # sql = "update ourydc_app_new_package set dt='2021-10-19',status=1"
    r = MysqlDbUtil().query(sql) 
    print(r)
 
        

