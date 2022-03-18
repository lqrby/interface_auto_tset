import xlrd,time,pymysql
from datetime import date,datetime
from db_util import MysqlDbUtil
from warnings import filterwarnings


# filterwarnings("ignore",category=pymysql.Warning)
# def read_excel():
#     # 打开文件
#     workbook = xlrd.open_workbook('C:/Users/lika/Desktop/5.4.5接口测试用例.xlsx')
#     # 根据sheet索引或者名称获取sheet内容
#     sheet = workbook.sheet_by_index(0)
#     for row in range(sheet.nrows):
#         if row == 0:
#             continue
#         ncols = sheet.row_values(row)
#         sql = "INSERT INTO apitest_case \
#             ( version,url_name,domain_or_ipaddress,port,url,method,case_number,parameter_interpretation,variable_parameters,request_parameters,interface_status,run,expect_result,response,pass_or_not,update_time,remark) \
#             VALUES \
#             ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',now(),'{}')".format(
#                 ncols[0],ncols[1],ncols[2],ncols[3],ncols[4],ncols[5],ncols[6],ncols[7],ncols[8],ncols[9],ncols[10],ncols[11],ncols[12],ncols[13])
#         res = MysqlDbUtil().execute(sql)
#         if res:
#             print("插入数据成功")
#         else:
#             print("插入数据失败=======",res)
#         time.sleep(1)




