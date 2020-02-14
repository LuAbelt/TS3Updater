import ts3updater.Version as updater
from ts3updater.Updater import Updater


def main():
    up = Updater("/home/lukas/TS3", "/home/lukas/backup")
    up.perform_update(True, True)


if __name__ == "__main__":
    main()
