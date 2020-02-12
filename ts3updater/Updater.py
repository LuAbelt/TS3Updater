from ts3updater.Version import VersionChecker
import os
import wget


class Updater:

    def __init__(self, install_dir: str, backup_dir: str):
        if type(install_dir) is not str:
            raise TypeError("install_dir must be of type str!")
        if type(backup_dir) is not str:
            raise TypeError("backup_dir must be of type str!")

        self.install_dir = install_dir
        self.backup_dir = backup_dir
        self.__DOWNLOAD_BASE_URL = "https://files.teamspeak-services.com/releases/server/%VERSION%/teamspeak3" \
                                   "-server_linux_amd64-%VERSION%.tar.bz2 "

    def perform_update(self, create_backup: bool, update_major: bool):
        version_checker = VersionChecker(self.install_dir)

        if not version_checker.requires_update():
            return True

        cur_version = version_checker.get_installed_version()
        latest_version = version_checker.get_latest_version()

        if not update_major and cur_version.major < latest_version.major:
            return True

        download_url = self.__DOWNLOAD_BASE_URL.format(latest_version)
        tmpfile = os.tmpfile()
        wget.download(download_url, tmpfile)
