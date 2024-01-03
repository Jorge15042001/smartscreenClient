import serial
import threading
from time import sleep


class SerialClient:
    def __init__(self, port, bdrate):
        self.port = port
        self.bdrate = bdrate
        self.moving = False
        self.channel = serial.Serial(self.port, self.bdrate)
        print("waitting for response serial")
        final_height = self.channel.readline()
        print("got height")
        final_height = int(final_height)
        self.height = final_height

    def move(self, rel_height: int):
        rel_height = round(rel_height * 10)

        # TODO: add proper signals or lock
        while self.moving:
            print("Waiting for serial port to become avialable")
            sleep(0.5)
        self.moving = True

        def run_movement():
            self.channel.write(
                f"x:0,y:0,z:{rel_height + self.height};R:0,P:0,Y:0".encode("utf-8"))
            final_height = self.channel.readline()
            final_height = int(final_height)
            self.height = final_height
            self.moving = False
        threading.Thread(target=run_movement).start()
