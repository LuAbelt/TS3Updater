# Steps required:
# 1. Get current installed version
# 2. Get latest release
# 3. Download latest version
# 4. Stop running server
# 5. Backup old teamspeak folder
# 6. Unpack new teamspeak
# 7. Start server
# 8. Check if server is running (optional)
import bs4
import os
import re
import requests

VERSION_REGEX = re.compile(r'(\d+\.\d+\.\d+)')


class TSVersion:
    def __init__(self, major: int, minor: int, fix: int):
        self.major = major
        self.minor = minor
        self.fix = fix

    def __init__(self, version: str):
        if type(version) is not str:
            raise TypeError("version is not of type string!")

        if not re.match(VERSION_REGEX, version):
            raise ValueError("Version does not match correct format. Required format: 'MAJOR.MINOR.FIX'(e.g. '1.2.3')")

        versions = version.split(".")
        self.major = versions[0]
        self.minor = versions[1]
        self.fix = versions[2]

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.fix == other.fix

    def __lt__(self, other):
        if self.major < other.major:
            return True

        if self.major > other.major:
            return False

        if self.minor < other.minor:
            return True

        if self.minor > other.minor:
            return False

        if self.fix < other.fix:
            return True

        return False


class VersionChecker:

    def __init__(self, ts3_directory):
        self.__version_check_link = "https://www.teamspeak.de/download/teamspeak-3-amd64-server-linux/"
        self.ts3_dir = ts3_directory

    def get_installed_version(self):
        changelog_file = os.path.join(self.ts3_directory, "CHANGELOG")

        if not os.path.exists(changelog_file):
            raise ValueError("Changelog file not found!")

        f = open(changelog_file, "r")
        chlog_text = f.read()
        f.close()

        version_matches = re.findall(VERSION_REGEX, chlog_text)

        return TSVersion(version_matches[0])

    def get_latest_version(self):
        data = requests.get(self.__version_check_link)
        soup = bs4.BeautifulSoup(data.text, "html.parser")
        element = soup.select("[itemprop=softwareVersion]")
        version = element[0].text

        return TSVersion(version)

    def requires_update(self):
        current = self.get_installed_version()
        latest = self.get_latest_version()

        return latest > current
