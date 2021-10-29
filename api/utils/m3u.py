import re
from dataclasses import dataclass
from logging import getLogger
from typing import List

logger = getLogger('M3U')


@dataclass
class M3UMedia:
    title: str
    tvg_name: str
    tvg_ID: str
    tvg_logo: str
    tvg_group: str
    link: str


class M3UParser:
    """Mod from https://github.com/Timmy93/M3uParser/blob/master/M3uParser.py"""

    def __init__(self, content: str = None):
        self.lines: List[str] = []
        self.data: List[M3UMedia] = []

        if content is not None:
            self.read_data(content)

        if self.lines:
            self.scan_all()

    def read_data(self, content: str):
        self.lines = [line.rstrip('\n') for line in content.splitlines()]

    def scan_all(self):
        for index, line in enumerate(self.lines):
            if line.startswith('#EXTINF'):
                self.process_ext_inf(index)

    def process_ext_inf(self, n):
        line_info = self.lines[n]
        line_link = self.lines[n + 1]
        m = re.search("tvg-id=\"(.*?)\"", line_info)
        tid = m.group(1)
        m = re.search("tvg-logo=\"(.*?)\"", line_info)
        logo = m.group(1)
        m = re.search("group-title=\"(.*?)\"", line_info)
        group = m.group(1)
        m = re.search("[,](?!.*[,])(.*?)$", line_info)
        title = m.group(1)
        self.data.append(M3UMedia(title, '', tid, logo, group, line_link))
