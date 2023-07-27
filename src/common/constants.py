from typing import Final

# Mavis constant value
MAVIS_REPO: Final[str] = "mavis"
MAVIS_OWNER: Final[str] = "pnetwork"
MAVIS_MAIN_BRANCH: Final[str] = "master"

# Regular Expression
FINDALL_MICROSVC_APPVERSION_RE: Final[str] = "[^ ]- name: (.+?)\n.*?appVersion: (.*?)\n"
FIND_SPECIFY_MICROSVC_RE: Final[str] = "[^ ]- name: {}\n.*?appVersion: (?P<appVersion>.*?)\n"
