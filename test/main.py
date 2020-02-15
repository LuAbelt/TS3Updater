from ts3updater.Updater import Updater
import os

def start():
    print("Starting")
    start_cmd="~/TS3/ts3server_startscript.sh start"
    os.system(start_cmd)


def stop():
    print("Stopping")
    stop_cmd="~/TS3/ts3server_startscript.sh stop"
    os.system(stop_cmd)


def main():
    up = Updater("/home/lukas/TS3", stop, start, "/home/lukas/backup")
    up.perform_update(True, True)


if __name__ == "__main__":
    main()
