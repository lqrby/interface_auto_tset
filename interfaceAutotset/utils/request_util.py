
import requests
from requests_toolbelt import MultipartEncoder


class RequestUtil:

    def __init__(self):
        pass

    def customRequest(self, url, method, headers=None, param=None, content_type=None):
        """
        通用请求工具类
        """
        try:
            if method == "post":
                if content_type == "multipart/form-data":
                    m = MultipartEncoder(param)
                    headers['Content-Type'] = m.content_type
                    result = requests.post(url=url, data=m, headers=headers, verify= False)
                    return result
                else:
                    result = requests.post(url=url, data=param, headers=headers, verify=False)
                    return result
            elif method == "get":
                result = requests.get(url=url, params=param, headers=headers, verify= False)
                return result
            else:
                print("http method not allowed")
        except Exception as e:
            print("http请求报错:{0}".format(e))

if __name__ == "__main__":
    r = RequestUtil()
    # url = "http://123.57.42.55:20800/api/newWebApi/annualCeremony/main"
    url = "http://123.57.42.55:20100/api/newApi/chatRoom/switchSeat"
    
    snatchChatRoom_data = {
        "common":{
            "appVersion":"5.4.91",
            "deviceGroupId":"android",
            "device":{
                "udid":"OPPO_PEGM00",
                "deviceId":"1E91B0B8243AA9335C7EF18368B5F7D4",
                "androidId":"8dbd0cf380f13f5a",
                "mac":"02:00:00:00"
            },
            "projectId":"ybb",
            "systemVersion":"30",
            "userId":"0002021062602142345000",
            "channelId":"YBB_beta",
            "token":""
        },
        "options":{
            "type":"2",
            "roomId":"406116000"
        }
    }

    
    header = {
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    results = r.customRequest(url,'post',param=snatchChatRoom_data, headers=header)
    print(results)