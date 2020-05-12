from locust import HttpLocust,Locust, TaskSet, task, seq_task
import sys
sys.path.append("F:/myTestFile/TestObject/YouTime")
from yunqianbao.qianMing import GetDataSign
class PublicRequest(TaskSet):

    def requestMethod(self,url,data,header):
        with self.client.post(url, data = data, headers = header, verify = False, allow_redirects=False,catch_response=True) as response:
                # result = json.loads(response.text)
                # if 'status' in result and result["status"] == 200 or 'status' in result and result["status"] == "200":
                #     time.sleep(random.randint(1,3))
                #     response.success()
            #推荐使用这种方式统计一个接口的响应时间，准确性更高
            return response
                # else:
                #     print("报错url==={} ，参数==={} ，报错原因==={}".format(url,data,result))
                #     response.failure("报错url==={} ，参数==={} ，报错原因==={}".format(url,data,result))
                    


