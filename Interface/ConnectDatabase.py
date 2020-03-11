import pymysql
#1连接数据库
def queryCursos():
    conn=pymysql.connect(host='192.168.1.26',port=3306,user='time',password='time25!QAZ',db='db_timebank',charset='utf8')
    #2获取游标
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor,conn