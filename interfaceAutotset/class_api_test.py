import sys, datetime, json,ast,random,requests,time
from utils.request_util import RequestUtil
from utils.db_util import MysqlDbUtil
# from customInterface.find_dependent_data import DependentData
from customInterface.query_data_base import DependentData
from user_data import userItems
from utils.checksum import CheckSumBuilder

class ClassTestCase:

    def __init__(self):
        self.requestUtil = RequestUtil()
        self.mysqlDbUtil = MysqlDbUtil()
        self.dependentData = DependentData()
        self.CheckSumBuilder = CheckSumBuilder()

    def loadAllCase(self):
        """
        根据接口状态加载全部用例
        """
        print("loadAllClassByApp")
        sql = "select * from `apitest_case` where run = 'yes' and interface_status = 0"
        results = self.mysqlDbUtil.query(sql)
        return results


    def findCaseById(self,case_id):
        """
        根据id找测试用例
        """
        print("findCaseById")
        sql = "select * from `apitest_case` where id = '{0}'".format(case_id)
        results = self.mysqlDbUtil.query(sql, state="one")
        return results


    def clearLastResultById(self,case_id):
        """
        根据测试用例id，清空上次结果
        """
        print("clearLastResultById")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "update `apitest_case` set response='', pass_or_not=0, update_time='{}' where id={}".format(current_time,case_id)
        rows = self.mysqlDbUtil.execute(sql)
        return rows

    def updateResultByCaseId(self,response,is_pass,case_id):
        """
        根据测试用例id，更新响应内容和测试内容
        """
        print("updateResultByCaseId")
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = str(response)[0:256]
        response = self.mysqlDbUtil.conn.escape_string(response)
        sql = "update apitest_case set response=\"{}\", pass_or_not='{}', update_time='{}' where id={}".format(response,is_pass,current_time,case_id)
        rows = self.mysqlDbUtil.execute(sql)
        if rows:
            print("更新完成")
        else:
            print("XXXXXX更新失败！XXXXXX")

    def runAllCase(self):
        """
        执行全部用例的入口
        """
        print("runAllCase")
        results = self.loadAllCase()
        for case in results:
            try:
                reponse = self.runCase(case)
                is_pass = self.assertResponse(case, reponse)
                self.updateResultByCaseId(reponse, is_pass, case["id"])
            except Exception as e:
                print("用例id={0},接口名称:{1},执行报错:{2}".format(case["id"],case["url_name"],e))



    def runSelectAllCase(self,caseid_list):
        """
        执行全部选中的用例
        """
        print("runSelectAllCase")
        for case_id in caseid_list:
            case = self.findCaseById(case_id)
            if case["run"] == "yes" and case["interface_status"] == 0:
                try:
                    self.clearLastResultById(case_id)
                    reponse = self.runCase(case)
                    is_pass = self.assertResponse(case, reponse)
                    self.updateResultByCaseId(reponse, is_pass, case["id"])
                except Exception as e:
                    print("用例id:{},接口名称:{},执行报错:{}".format(case["id"],case["url_name"],e))
            else:
                print("未执行,原因:已废弃、已关闭或限制执行")
                msg = "未执行,原因:已废弃、已关闭或限制执行"
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                sql = 'update apitest_case set remark="{}",update_time="{}" where id={}'.format(msg,current_time,case_id)
                rows = self.mysqlDbUtil.execute(sql)
                if rows:
                    print("更新完成")
                else:
                    print("XXXXXX更新失败！XXXXXX")


    def runCase(self,case):
        """
        执行单个用例
        """
        print("runCase")
        requestData = case.get("request_parameters")
        requestData = str(requestData).replace('_x000D_','')
        # print(66666,type(requestData),requestData)
        request_data=""
        try:
            request_data = ast.literal_eval(requestData)
            request_data
        except:
            print("请求参数格式错误")
            return "请求参数格式错误"
        interface_status = case["interface_status"]
        id = case["id"]
        run = case["run"]
        domain = case["domain_or_ipaddress"]
        port = case["port"]
        method = case["method"]
        url = case["url"]
        field = case["pre_fields"]
        headers = case["headers"]
        pre_fields={}
        try:
            pre_fields = json.loads(field)
        except:
            print("依赖参数格式错误！")
            return "依赖参数格式错误！"
        userItem = random.choice(userItems)
        print("user=======",userItem)
        if request_data and request_data.get("common"):
            if "userId" in request_data.get("common"):
                request_data["common"]["userId"] = userItem.get("user_id")
            if "token" in request_data.get("common"):
                request_data["common"]["token"] = userItem.get("pwd")
        if request_data and request_data.get("options"):
            user = self.dependentData.getData(1)
            if "userId" in request_data["options"]:
                request_data["options"]["userId"] = user.get("user_id")
            if request_data["options"].get("token"):
                request_data["options"]["token"] = user.get("pwd")
        msg = ""
        if run == "yes" and interface_status == 0:
            pre_case_id = case.get("pre_case_id")
            if pre_case_id > 100:
                print("有前置用例,id:{}".format(pre_case_id))
                pre_case = self.findCaseById(pre_case_id) #
                assert_type = case["assert_type"]
                #递归调用
                pre_response = self.runCase(pre_case)
                #前置条件断言
                pre_assert_msg = self.assertResponse(pre_case,pre_response)
                if pre_assert_msg == 2:
                    #前置条件不通过直接返回
                    msg = "用例(id={})未执行，前置用例(id={})不通过，响应值：{}".format(id,pre_case_id,pre_response)
                    return msg
                #处理响应值返回类型
                resultData = self.response_value_processing(pre_response,assert_type,pre_fields)
                if resultData != "not":
                    if not resultData:
                        msg = "用例(id={})未执行，前置用例(id={})无数据，响应值：{}".format(id,pre_case_id,pre_response)
                        return msg
                    try:
                        print("前置用例返回值：=======",resultData)
                        for key in pre_fields.keys():
                            if key != "result":
                                for okey in pre_fields[key].keys():
                                    request_data[key][okey] = resultData[pre_fields[key][okey]]
                    except:
                        print("请检查前置字段参数key拼写错误")
                        return "请检查前置字段参数key拼写错误"
            elif pre_case_id > 0 and pre_case_id <= 100:
                mysqlFindData = self.dependentData.getData(pre_case_id)
                if mysqlFindData:
                    try:
                        for key in pre_fields.keys():
                            for okey in pre_fields[key].keys():
                                request_data[key][okey] = mysqlFindData[pre_fields[key][okey]]
                    except:
                        print("请检查前置字段参数key拼写错误")
                        return "请检查前置字段参数key拼写错误"
                else:
                    print("数据库数据为空！！！！！")
                    return "数据库数据为空！！！！！"
            req_url = domain + ":" + str(port) + url
            if port != 20020:
                request_data = json.dumps(request_data)
            if headers:
                headers = json.loads(headers)
                auto_headers = self.CheckSumBuilder.getHeaders()
                for p_key,p_value in auto_headers.items():
                    if headers.get(p_key):
                        headers[p_key] = p_value
                print("headers===",headers)
            print("url===",req_url)
            print("data===",request_data)
            scr_result = self.requestUtil.customRequest(req_url,method,param=request_data,headers=headers)
            if "200" in str(scr_result):
                return scr_result.text
            else:
                print("状态码错误：{}".format(scr_result))
                return scr_result
        else:
            print("用例id:{}已废弃、已关闭或限制了运行".format(id))
            msg = "用例id:{}已废弃、已关闭或限制了运行".format(id)
            return msg


    def assertResponse(self,case,response):
        """
        断言响应内容，更新用例执行情况
        """
        print("assertResponse")
        expectResult = str(case["expect_result"])
        expect_results = expectResult.split("#")
        is_pass = 2
        # if not response:
        #     return is_pass
        try:
            json_response = json.loads(response)
        except:
            json_response=response
        res = ""
        if 'common' in json_response:
            res = json_response['common']['desc']
        elif 'msg' in json_response:
            res = json_response['msg']
        else:
            res = json_response
        
        for expect_result in expect_results:
            if expect_result in res:
                is_pass = 1
                break
        return is_pass


    '''
    接口响应值根据类型进行处理并返回
    '''
    def response_value_processing(self,response,assert_type,pre_fields):
        json_response = json.loads(response)
        res_num = json_response.get("common").get("reset") #响应码
        if str(res_num) == "21000":
            return self.options_list(json_response,pre_fields.get("result"))
        else:
            print("响应码非21000")
            return False
        
    
    def options_list(self,json_response,list_key): 
        resultList = {}
        res_options = json_response.get("options")
        if list_key:
            one_level_key = list(list_key.keys())[0]
            if list_key.get(one_level_key):
                one_level = list_key.get(one_level_key)
                two_level_key = list(one_level)[0]
                if list_key[one_level_key].get(two_level_key):
                    two_level = one_level.get(two_level_key)
                    three_level_key = list(two_level)[0]
                    if list_key[one_level_key][two_level_key].get(three_level_key):
                        print("居然还有第四层")
                        return resultList
                    else:
                        resultList =  res_options[one_level_key][two_level_key][three_level_key]
                else:
                    resultList =  res_options[one_level_key][two_level_key]
            else:
                resultList =  res_options[one_level_key]
        else:
            resultList =  res_options
        item = random.choice(resultList)
        return item

    