from ts3updater.Version import VersionChecker
from typing import Callable
import tarfile
import os
import wget


class Updater:

    def __init__(self, install_dir: str, shutdown_command: Callable, start_command: Callable, backup_dir: str = None):
        if type(install_dir) is not str:
            raise TypeError("install_dir must be of type str")
        if backup_dir is not None and type(backup_dir) is not str:
            raise TypeError("backup_dir must be of type str")
        if not callable(shutdown_command):
            raise TypeError("shutdown_command needs to be of type Callable, is of type " + type(shutdown_command))
        if not callable(start_command):
            raise TypeError("start_command needs to be of type Callable")

        if not os.path.isdir(install_dir):
            raise ValueError("install_dir is not a valid directory")
        if backup_dir is not None and not os.path.isdir(backup_dir):
            print("Specified backup_dir not existent yet. Creating...")
            os.mkdir(backup_dir)

        self.install_dir = install_dir
        self.backup_dir = backup_dir
        self.shutdown_sever = shutdown_command
        self.start_server = start_command
        self.__DOWNLOAD_BASE_URL = "https://files.teamspeak-services.com/releases/server/%VERSION%/teamspeak3" \
                                   "-server_linux_amd64-%VERSION%.tar.bz2"

    def perform_update(self, create_backup: bool = True, update_major: bool = False):
        if create_backup and self.backup_dir is None:
            print("Warning: create_backup was True but no backup dir was specified!")
            create_backup = False

        version_checker = VersionChecker(self.install_dir)

        if not version_checker.requires_update():
            print("No update required")
            return True

        cur_version = version_checker.get_installed_version()
        latest_version = version_checker.get_latest_version()

        print("Current version: " + str(cur_version))
        print("Latest version: " + str(latest_version))

        if not update_major and cur_version.major < latest_version.major:
            return True

        download_url = self.__DOWNLOAD_BASE_URL.replace("%VERSION%", str(latest_version))
        print(download_url)
        tmp_file = str(latest_version) + ".tar.bz2"
        wget.download(download_url, tmp_file)

        self.shutdown_sever()

        if create_backup:
            backup_file = os.path.join(self.backup_dir, "TS3_{}_backup.tar.gz".format(str(cur_version)))
            self.backup(backup_file)

        print(self.install_dir)
        print(tmp_file)
        with tarfile.open(tmp_file, "r") as tar:
            top_level_dir = tar.getmembers()[0].path + "/"
            for member in tar.getmembers():
                if member.path.startswith(top_level_dir):
                    member.path = member.path[len(top_level_dir):]

            tar.extractall(self.install_dir)
            os.rmdir(os.path.join(self.install_dir, tar.getmembers()[0].path))

        self.start_server()

        os.remove(tmp_file)

    def backup(self, backup_file: str):

        with tarfile.open(backup_file, "w:gz") as tar:
            for root, dirs, files in os.walk(self.install_dir):
                for file in files:
                    tar.add(os.path.join(root, file))
