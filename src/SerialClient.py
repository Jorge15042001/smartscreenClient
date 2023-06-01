import serial
import threading


class SerialClient:
    def __init__(self, port, bdrate):
        self.port = port
        self.bdrate = bdrate
        self.channel = serial.Serial(self.port, self.bdrate)
        h = self.channel.readline()
        self.height = int(h) 

<<<<<<< HEAD
    def move(self, rel_height:float):
        #convert to mm from cm
        rel_height = round(rel_height * 10)
        def run_movement():
            self.channel.write(f"x:0,y:0,z:{self.height+rel_height},R:0,P:0,Y:0".encode("utf-8"))
=======
    def move(self, rel_height: int):
        def run_movement():
            self.channel.write(
                f"x:0;y:0;z:{rel_height};R:0;P:0;Y:0;".encode("utf-8"))
>>>>>>> 7afc94f2e82b7845230e1ab3d4993232561d0db7
            final_height = self.channel.readline()
            final_height = int(final_height)
            self.height = final_height
        threading.Thread(target=run_movement).start()
