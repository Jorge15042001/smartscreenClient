
from websockets.sync.client import connect
import threading
from time import sleep
import json
#import ssl
#ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

class ScreenSocketClient:
    def __init__(self, screen_id):
        self.screen_id = str(screen_id)
        self.url = f"ws://smartscreen.jorgevulgarin.cc:8001/ws/hardware_controller/{screen_id}/"
        self.status = "Active"
        self.ws_client = connect(self.url)
        self.status_reported_thread = threading.Thread(
            target=self.status_reporter)
        self.keep_loop = True

    def status_reporter(self):
        while self.keep_loop:
            json_str = json.dumps({
                'msg_type': "screenhardware.status",
                "screen": self.screen_id,
                "status": self.status,
            })
            self.ws_client.send(json_str)
            sleep(5)

    def start(self):
        self.status_reported_thread.start()

    def close(self):
        self.keep_loop = False
        self.ws_client.close()

    def alert_person_detected(self):
        json_str = json.dumps({
            "msg_type": "screenhardware.personconnected",
            "screen": self.screen_id,
        })
        print(json_str)
        self.ws_client.send(json_str)

    def alert_person_leaves(self):
        json_str = json.dumps({
            "msg_type": "screenhardware.personleaves",
            "screen": self.screen_id,
        })
        print(json_str)
        self.ws_client.send(json_str)

