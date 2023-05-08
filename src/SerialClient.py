import serial
import threading 


class SerialClient:
    def __init__(self, port, bdrate):
        self.port = port
        self.bdrate = bdrate
        self.channel = serial.Serial(self.port, self.bdrate)
        self.height = 1000

    def move(self, rel_height:int):
        def run_movement():
            self.channel.write(f"x:0;y:0;z:{rel_height};R:0;P:0;Y:0;".encode("utf-8"))
            final_height = self.channel.readline()
            final_height = int(final_height)
            self.height = final_height
        threading.Thread(target=run_movement).start()
