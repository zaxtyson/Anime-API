"""
LIB 在线: https://www.libvio.com/
"""
import json
import re
import time
from base64 import b64decode
from urllib.parse import urlparse, unquote

from api.core.anime import *
from api.core.proxy import AnimeProxy
from api.utils.tool import md5
from api.utils.logger import logger

# 解决验证码问题
Header = {"cookie": "PHPSESSID=qhvh9b4up839mrnr6pp90ci2sp"}


class LibVio(AnimeSearcher):

    async def search(self, keyword: str):
        api = "https://www.libvio.com/search/-------------.html"
        params = {"wd": keyword, "submit": ""}
        resp = await self.get(api, params=params, headers=Header)
        if not resp or resp.status != 200:
            return
        html = await resp.text()
        if "请输入验证码" in html:
            logger.warning("LibVio needs verification code")
            return
        rets = self.xpath(html, '//div[@class="stui-vodlist__box"]')
        for ret in rets:
            meta = AnimeMeta()
            meta.title = ret.xpath('a/@title')[0]
            meta.detail_url = ret.xpath('a/@href')[0]  # /detail/5060.html
            meta.cover_url = ret.xpath('a/@data-original')[0]
            meta.desc = ret.xpath('a/span[@class="pic-text text-right"]/text()')[0]
            yield meta


class LibVioDetailParser(AnimeDetailParser):

    async def parse(self, detail_url: str):
        detail = AnimeDetail()
        api = "https://www.libvio.com" + detail_url
        resp = await self.get(api, headers=Header)
        if not resp or resp.status != 200:
            return detail
        html = await resp.text()
        detail_info = self.xpath(html, '//div[@class="stui-content__detail"]')[0]
        detail.cover_url = self.xpath(html, '//a[@class="pic"]/img/@data-original')[0]
        detail.title = detail_info.xpath('h1[@class="title"]/text()')[0]
        detail.desc = detail_info.xpath('//span[@class="detail-content"]/text()')[0]
        category = detail_info.xpath('p[1]/text()')[0]
        detail.category = category.split('/')[0].replace('类型：', '')

        playlist_names = self.xpath(html, '//div[@class="stui-pannel__head clearfix"]/h3/text()')
        playlists = self.xpath(html, '//ul[@class="stui-content__playlist clearfix"]')
        for i, playlist in enumerate(playlists):
            pl = AnimePlayList()
            pl.name = playlist_names[i].replace(" ", "").replace("\r\n", "")
            data = playlist.xpath('.//li')
            for ep in data:
                anime = Anime()
                anime.name = ep.xpath('a/text()')[0]
                anime.raw_url = ep.xpath('a/@href')[0]  # /play/4988-1-11.html
                pl.append(anime)
            detail.append_playlist(pl)
        return detail


class LibVioUrlParser(AnimeUrlParser):

    @staticmethod
    def get_signed_url(url: str) -> str:
        """计算 URL 的签名"""
        # 加密算法见: https://www.libvio.com/static/img/load.html
        # 代码使用 sojson v6 进行混淆
        path = urlparse(url).path
        t = format(int(time.time()) + 300, 'x')  # 时间戳的十六进制表示
        key = "y4nZpZYXK7SOr3wWlvyD0RTl8ti61IbeVFTjpLQv21hPKKTy"
        sign = md5(key + path + t).lower()
        return f"{url}?sign={sign}&t={t}"

    @staticmethod
    def get_decode_url(url: str) -> str:
        """有些url被编码过, 还原"""
        url = unquote(url)

        # 有些被 base64 编码的 url=JTY4JTc0JTc0JTcwJTczJTNBJTJGJT...
        if not url.startswith("http"):
            # 得到 url编码 url=%68%74%74%70%73%3A%2F%2F%76%6F
            url = b64decode(url).decode()
            url = unquote(url)
        return url

    async def parse(self, raw_url: str):
        api = "https://www.libvio.com" + raw_url
        resp = await self.get(api, headers=Header)
        if not resp or resp.status != 200:
            return ""
        html = await resp.text()
        data = re.search(r"player_aaaa=({.+?})<", html)
        if not data:
            return ""
        data = json.loads(data.group(1))
        url = self.get_decode_url(data["url"])
        url = self.get_signed_url(url)
        return AnimeInfo(url, lifetime=300)


class LibVioProxy(AnimeProxy):

    # TODO: duoduozy.com m3u8 player
    def set_proxy_headers(self, url: str) -> dict:
        if "duoduozy.com" in url:
            return {"Origin": "https://dp.duoduozy.com"}

    def enforce_proxy(self, url: str) -> bool:
        if "chinacloudapi.cn" in url:
            return True
        if "duoduozy.com" in url:
            return True
        return False

    def fix_chunk_data(self, url: str, chunk: bytes) -> bytes:
        if "duoduozy.com" in url:
            return chunk[0x303:]  # 前面是图片数据
        return chunk
