from stereoHeight.height_estimation.height_stimation import HeightDaemon
from screenSocketClient import ScreenSocketClient
from SerialClient import SerialClient


if __name__ == "__main__":
    """Program entry point
    """
    screen_id = 2  # this value should be checked in the admin screen
    # send information about current state of the screen to the server
    socket_client = ScreenSocketClient(screen_id)
    # used for communication with the height control module
    serial_client = SerialClient("/dev/ttyACM0", 115200)

    socket_client.start()  # start communication with server

    # Height estimation deamon
    height_damemon = HeightDaemon("./config_files/stereo_config.json")

    # callback for person seen
    def person_seen_callback(rel_height):
        serial_client.move(rel_height)

    # callback for person detected
    def person_detected_callback(rel_height):
        socket_client.status = "Waiting"
        socket_client.alert_person_detected()
        serial_client.move(rel_height)

    # callback for person leaves screen
    def person_leaves_callback():
        socket_client.status = "Active"
        socket_client.alert_person_leaves()

    # set callbacks on the HeightDaemon
    height_damemon.set_on_person_seen(person_seen_callback)
    height_damemon.set_on_person_detected(person_detected_callback)
    height_damemon.set_on_person_leaves(person_leaves_callback)

    print("height daemon starting")
    # starting height daemon
    height_damemon.start()
    print("height daemon started")
    exit_main_loop = False
    while not exit_main_loop and height_damemon.keep_loop:
        print(not exit_main_loop and height_damemon.keep_loop)
        # enter 'q' to close program also close if the height_damemon stops
        exit_main_loop = input("Enter 'q' to exit: ") == 'q'
    height_damemon.close()
    socket_client.close()
