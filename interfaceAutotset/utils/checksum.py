
import hashlib, time
class CheckSumBuilder():

    def getCheckSum(self,appSecret, nonce, curTime):
        
        """
        使用sha1加密算法，返回str加密后的字符串
        """
        res = appSecret + nonce + curTime
        sha = hashlib.sha1(res.encode('utf-8'))
        encrypts = sha.hexdigest()
        return encrypts

# if __name__ == '__main__':
#     AppKey = "7ca5cef23fd00cb4774107175ab6d413"
#     appSecret = "eb1b96102f93"
#     nonce = str(int(time.time() * 1000))
#     curTime = str(int(time.time()))
#     res = CheckSumBuilder().getCheckSum(appSecret, nonce, curTime)
#     print(res)


    def getHeaders(self):
        
        """
        使用sha1加密算法，返回str加密后的字符串
        """
        AppKey = "7ca5cef23fd00cb4774107175ab6d413"
        appSecret = "eb1b96102f93"
        nonce = str(int(time.time()*1000))
        curTime = str(int(time.time()))

        res = appSecret + nonce + curTime
        sha = hashlib.sha1(res.encode('utf-8'))
        checkSum = sha.hexdigest()
        headers ={
            "Content-Type":"application/x-www-form-urlencoded;charset=utf-8",
            "AppKey":AppKey,
            "Nonce":nonce,
            "CurTime":curTime,
            "CheckSum":checkSum
        }
        return headers


        
        
        