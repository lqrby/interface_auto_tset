from .ConnectDatabase import queryCursos

def queryUsers():
    '''
    #3执行查询，并获取查询的用户总行数
    '''
    cursor,conn = queryCursos()
    rowNums = cursor.execute('SELECT id,nickname,mobile FROM tb_user limit 27,220')
    print('查询的行数为' + str(rowNums))
    #4.遍历结果，获取查询的结果
    ResultList = cursor.fetchall()
    for i in range(len(ResultList)):
        print(ResultList[i])
    #提交如果需要插入语句的时候使用commit
    #conn.commit()
    #关闭
    cursor.close()
    conn.close()
    return ResultList
# queryUsers()