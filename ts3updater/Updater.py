import tempfile

from ts3updater.Version import VersionChecker
import os
import wget


class Updater:

    def __init__(self, install_dir: str, backup_dir: str = None):
        if type(install_dir) is not str:
            raise TypeError("install_dir must be of type str")
        if backup_dir is not None and type(backup_dir) is not str:
            raise TypeError("backup_dir must be of type str")

        if not os.path.isdir(install_dir):
            raise ValueError("install_dir is not a valid directory")

        if backup_dir is not None and not os.path.isdir(backup_dir):
            raise ValueError("backup_dir is not a valid directory")

        self.install_dir = install_dir
        self.backup_dir = backup_dir
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
        tmp_file = os.path.join(tempfile.gettempdir(), str(latest_version) + ".tar.bz2")
        print(tmp_file)
        wget.download(download_url, tmp_file)

        #Next steps:
        # 1. Shutdown old server
        # 2. Create Backup
        # 3. Unpack new version
        # 4. Start Server
