__all__ = ["get_sources", "TVSource"]

from typing import List

from api.core.helper import HtmlParseHelper
from api.utils.m3u import M3UParser


class TVSource(object):

    def __init__(self, name: str, logo_url: str, url: str):
        self.name = name
        self.logo_url = logo_url
        self.url = url

    def __repr__(self):
        return f"<TV {self.name}>"


async def get_sources() -> List[TVSource]:
    """获取 IPTV 源"""
    fetcher = HtmlParseHelper()
    await fetcher.init_session()
    resp = await fetcher.get('https://iptv-org.github.io/iptv/countries/cn.m3u')
    if not resp or resp.status != 200:
        return []
    m3u_data = await resp.text()
    p = M3UParser(m3u_data)

    return [
        TVSource(
            name=media.title,
            logo_url=media.tvg_logo,
            url=media.link,
        )
        for media in p.data
    ]
