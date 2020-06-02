from locust import Locust, TaskSet, task
from gevent import monkey
import random
import string
import time
import json
from locustWebSocket import LocustWebSocketClient


class UserBehavior(TaskSet):
    def on_start(self):
        self.user_id_list = []
        self.all_sid = get_sid()
        self.url = 'ws://121.40.165.18:8800'
        all_worker_info = worker_contract_list(get_ws_driver(ws_url=self.url), self.all_sid[0][0], flag=1,
                                               limit='15', page=1, project_id=self.all_sid[0][1], request_status='完成',
                                               status=0, with_charkt_value=True)
        for worker_info in all_worker_info['data']['worker_contract']:
            self.user_id_list.append(worker_info['id'])
        print(self.user_id_list)
        
 
    @task
    def test_project1(self):
        ws = LocustWebSocketClient(self.url)
        project_list(ws_driver=ws, sid=self.all_sid[0][0])
        ws.ws.close()
class WebUserLocust(LocustWebSocketClient):
    weight = 1
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 7000
