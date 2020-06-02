from locust import Locust, events, task, TaskSet

import websocket

import time

import gzip

 

class WebSocketClient():

    def __init__(self, host):

        self.host = host

        #self.port = port

 

class WebSocketLocust(Locust):

    def __init__(self, *args, **kwargs):

        self.client = WebSocketClient("172.31.15.85")

 

class UserBehavior(TaskSet):

 

    # ws = websocket.WebSocket()

    # #self.ws.connect("ws://10.98.64.103:8807")

    # ws.connect("ws://pro-web-new.devtest.exshell-dev.com/r1/main/ws")

 

    @task(1)

    def buy(self):

        try:

            ws = websocket.WebSocket(environ, socket, rfile)

            # self.ws.connect("ws://10.98.64.103:8807")

            ws.connect("https:// testawss.bankft.com/wss")
            #  ws.connect("ws://pro-web-new.devtest.exshell-dev.com/r1/main/ws")

 

            start_time = time.time()

 

            #self.ws.send('{"url":"/buy","data":{"id":"123","issue":"20170822","doubled_num":2}}')

            #result = self.ws.recv()

 

            send_info = '{"sub": "market.ethusdt.kline.1min","id": "id10"}'

            # send_info = '{"event":"subscribe", "channel":"btc_usdt.deep"}'

            while True:

                # time.sleep(5)

                # ws.send(json.dumps(send_info))

                ws.send(send_info)

                while (1):

                    compressData = ws.recv()

                    result = gzip.decompress(compressData).decode('utf-8')

                    if result[:7] == '{"ping"':

                        ts = result[8:21]

                        pong = '{"pong":' + ts + '}'

                        ws.send(pong)

                        ws.send(send_info)

                     # else:

                    #     # print(result)

                    #     with open('./test_result.txt', 'a') as f:

                    #         #f.write(threading.currentThread().name + '\n')

                    #         f.write(result + '\n')

        except Exception as e:

            print("error is:",e)

 

class ApiUser(WebSocketLocust):

    task_set = UserBehavior

    min_wait = 100

    max_wait = 200

 