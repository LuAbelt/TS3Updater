import ts3updater.Version as updater
from ts3updater.Updater import Updater


def start():
    print("Starting")


def stop():
    print("Stopping")


def main():
    up = Updater("/home/lukas/TS3", stop, start, "/home/lukas/backup")
    up.perform_update(True, True)


if __name__ == "__main__":
    main()
