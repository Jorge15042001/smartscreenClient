from stereoHeight.height_estimation.height_stimation import HeightDaemon
from screenSocketClient import ScreenSocketClient
from SerialClient import SerialClient


if __name__ == "__main__":
    screen_id = 1
    socket_client = ScreenSocketClient(screen_id)
    serial_client = SerialClient("/dev/ttyACM0", 9200)

    socket_client.start()

    height_damemon = HeightDaemon("./config_files/stereo_config.json")

    def person_detected_callback(rel_height):
        socket_client.status = "Waiting"
        socket_client.alert_person_detected()
        serial_client.move(rel_height)

    def person_leaves_callback():
        socket_client.status = "Active"
        socket_client.alert_person_leaves()

    height_damemon.set_on_person_detected(person_detected_callback)
    height_damemon.set_on_person_leaves(person_leaves_callback)

    height_damemon.start()
    exit_main_loop = False
    while not exit_main_loop and height_damemon.keep_loop:
        print(not exit_main_loop and height_damemon.keep_loop)
        exit_main_loop = input("Enter 'q' to exit: ") == 'q'
    height_damemon.close()
    socket_client.close()
