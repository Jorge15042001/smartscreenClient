from stereoHeight.height_estimation.height_stimation import HeightDaemon
from websockets.sync.client import connect
import threading
from time import sleep
import json

screen_id = 8


class ScreenSocketClient:
    def __init__(self, screen_id):
        self.screen_id = str(screen_id)
        self.url = f"ws://localhost:8000/ws/hardware_controller/{screen_id}/"
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


if __name__ == "__main__":
    s_client = ScreenSocketClient(screen_id)
    s_client.start()

    height_damemon = HeightDaemon("./config_files/stereo_config.json")

    def person_detected_callback():
        s_client.status = "Waiting"
        s_client.alert_person_detected()

    def person_leaves_callback():
        s_client.status = "Active"
        s_client.alert_person_leaves()

    height_damemon.set_on_person_detected(person_detected_callback)
    height_damemon.set_on_person_leaves(person_leaves_callback)

    height_damemon.start()
    exit_main_loop = False
    while not exit_main_loop and height_damemon.keep_loop:
        print(not exit_main_loop and height_damemon.keep_loop)
        exit_main_loop = input("Enter 'q' to exit: ") == 'q'
    height_damemon.close()
    s_client.close()
