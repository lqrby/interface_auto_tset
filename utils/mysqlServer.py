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

class MysqlDb:
    def __init__(self):
        #建立数据库连接
        self.conn = pymysql.connect(host='123.57.42.55',port=3306,user='ourydcdbtestuser',password='2y3218ASfRdCK2Q1',db='ourydcdbtest',charset='utf8')
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


    def __del__(self):
        #关闭游标
        self.cur.close()
        #关闭连接
        self.conn.close()

    def query(self, sql, state="all"):
        """
        查询
        """
        self.cur.execute(sql)
        # data = {}
        if state == "all":
            data = self.cur.fetchall()
        else:
            data = self.cur.fetchone()
        return data


    def execute(self, sql):
        """
        更新、修改、删除
        """
        try:
            print("sql=======",sql)
            #使用execute操作sql
            rows = self.cur.execute(sql)
            #提交事务
            self.conn.commit()
            return True
        except Exception as e:
            print("数据库操作异常:{}".format(e))
            #事务回滚修改
            self.conn.rollback() 
        

if __name__ == "__main__":
    # r = MysqlDb().query("select * from `case`"
    # sql = "INSERT INTO `case` (app,module,run) VALUES('youtime','user','yes');"
    # sql = "select room_id from ourydc_app_chat_room where identity_id='99883'"  #查询房间id
    # sql = "select room_id from ourydc_app_chat_room where room_manager = '8a9bcb4c6aa5617d016aa59b74dc044e'"
    # sql = "select * from ourydc_app_chat_room where room_id = '104972572'"
    # sql = "update ourydc_app_new_package set dt='2021-10-19',status=1"
    sql = "select room_id,room_state from ourydc_app_chat_room where room_id = '99883'"
    r = MysqlDb().query(sql) 
    print(r)
 
        

