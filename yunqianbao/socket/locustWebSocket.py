from locust import Locust,TaskSet,task
from locust import events
from gevent import monkey
from websocket import create_connection
import random
import string
import time
import json






class LocustWebSocketClient(Locust):
    def __init__(self, ws_url, callback=None):
        super().__init__()
        self.ws = create_connection(ws_url, timeout=10)
        self.ws_url = ws_url
        self.callback = callback
 
    def web_socket_request(self, dictmsg):
        resp = None
        total_time = None
        try:
            start_time = time.time()
            print('send:', dictmsg)
            self.ws.send(simplejson.dumps(dictmsg))
            result = self.ws.recv()
            resp = simplejson.loads(result)
            print("recv:", resp)
            total_time = int((time.time() - start_time) * 1000)
            if resp['code'] == (1001 or 1000 or 1002):
                pass
            else:
                print('error send:', dictmsg, 11111)
                events.request_failure.fire(
                    request_type='wss',
                    name='web_socket_request',
                    response_time=total_time,
                    exception=resp
                )
            events.request_success.fire(
                request_type='wss',
                name='web_socket_request',
                response_time=total_time,
                response_length=len(resp)
            )
            if self.callback is None:
                return resp
            else:
                return self.ws
        except Exception as e:
            print(e)
            events.request_failure.fire(
                request_type='wss',
                name='web_socket_request',
                response_time=total_time,
                exception=resp
            )
