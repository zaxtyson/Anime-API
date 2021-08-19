.. _extension:

============
引擎模板
============

对于定向的资源爬取任务，往往有特定的模式可循。API 框架将视频、弹幕、小说、漫画、音乐
这些抓取任务的工作模式进行了抽象，将数据抓取、处理所需要的常用功能进行了封装，
减少编写引擎的难度。

框架会自动伪装每一个请求、对获取的数据加标记、过滤清洗，最后以统一的 JSON 接口展现出来。
数据的解析是逐步进行的，只有当你访问某个的接口时，它才会调度相关引擎去完成进一步的解析。
解析过程中某些数据会自动缓存，以加快处理速度。对于寿命短暂的直链，API 通过动态重定向为资源续命。
对于存在防盗链的资源，它也能作为代理服务器，访问原始数据流并返回响应给前端，完成视频的播放......

这里面有许多繁琐无聊的事情, 好在 API 框架为你做了这些脏活，你只需要按照特定的模式，
一步一步提取数据就好。但是，这仍然是一件具有挑战性的事情，
因为你无法预料目标网站或者APP使用了何种手段阻止你抓取数据，不知道它将某些关键参数藏到了哪里，
即便已经接近成功，它仍可能返回一些稀奇古怪的数据迷惑你。数据的抓取是最困难的事情，
你可能遇到网页端反调试、js加密、接口数据加密、APP加壳、资源数据混淆等等问题，
这里有不少的坑，我个人的一些经验总结在了
:ref:`爬虫技巧 <skills>` 一栏，
如果遇到问题，可以看看，说不定能得到启发。

OK，说了一大堆，现在我们终于要开始了！

现在，你盯上了一个网站或者APP，觉得它的资源很不错，可是广告满天飞，
于是你想把它做成一个引擎添加进来...

如何添加引擎
=====================

写好的引擎不要扔，裹上鸡蛋液，粘上面包糠, 扔到下面对应的目录下:

.. code-block::

    api
    ├─anime     # 视频搜索
    ├─danmaku   # 弹幕搜索
    ├─comic     # 漫画搜索
    └─music     # 音乐搜索

然后, 在 `api/config.json` 中增加一个对应的配置项, 如:

.. code-block:: json

    {
        "anime": [
            {
                "name": "歪比巴卜",
                "notes": "这里写点简介",
                "module": "api.anime.wbbb",
                "type": [
                    "动漫"
                ],
                "enable": false,
                "quality": 8
            }
        ]
    }


- `module` 是该引擎的模块名，与文件路径保持一致
- `enable` 表示是否启用该引擎
- `quality` 表示资源的整体质量 0~10 分

视频搜索引擎
======================
视频的搜索解析模板:

.. code-block:: python

    from api.core.anime import *
    from api.core.proxy import StreamProxy

    class MyEngine(AnimeSearcher):

        async def search(self, keyword: str):
            """
            实现本方法, 搜索剧集摘要信息, 返回异步生成器
            """
            html = "keyword 对应的网页内容"
            items = ["剧集1的摘要信息", "剧集2的摘要信息", "剧集3的摘要信息"]
            for item in items:
                meta = AnimeMeta()
                # 对 item 进行解析， 提取以下数据
                meta.title = "番剧名称"
                meta.category = "分类"
                meta.desc = "简介"
                meta.cover_url = "封面图 URL"
                meta.detail_url = "详情页链接或参数"
                yield meta  # 产生一个结果交给下一级处理


    class MyDetailParser(AnimeDetailParser):

        async def parse(self, detail_url: str):
            """
            实现本方法, 解析摘要信息中的链接， 获取详情页数据
            """
            detail = AnimeDetail()

            # detail_url 就是上面搜索结果中提取的内容
            # 从详情页提取以下信息
            detail.title = "番剧名称"
            detail.cover_url = "封面图 URL"
            detail.desc = "简介"
            detail.category = "分类"

            playlists = ["播放列表1的信息", "播放列表2的信息"]
            for playlist in playlists:
                pl = AnimePlayList()
                # 解析播放列表的 html， 提取播放列表名和列表内容
                pl.name = "播放列表名"
                for item in playlist:
                    anime = Anime()
                    # 解析列表中的一集视频， 提取视频名字和 URL 信息
                    anime.name = "某一集视频的名字"
                    anime.raw_url = "视频的原始链接或者参数"
                    pl.append(anime)
                detail.append_playlist(pl)
            return detail

    class MyUrlParser(AnimeUrlParser):

        async def parse(self, raw_url: str) -> Union[AnimeInfo, str]:
            """
            实现本方法, 解析某一集视频的原始链接, 获取直链和有效期
            如果在详情页已经提取到了有效的直链, 可以不写这个类, 但通常是需要的
            """
            # raw_url 是从详情页提取的信息
            real_url = "根据 raw_url 找到的视频直链"
            return real_url # 直接返回直链是可以的， 框架会尝试自行推断该直链对应的视频信息

            # 如果你知道这个直链的信息就最好不过了， 省得框架去推测， 因为这不一定准确
            # lifetime 视频的剩余寿命(秒)， 如果视频过期， 框架将重新解析一次直链
            # fmt 是视频格式, 可选 mp4 flv hls， 这将给前端播放器一个提示， 以便选择正确的解码器播放
            # volatile 表示视频直链是否在访问后立即失效， 如果为 True， 则每次前端请求视频数据时， 框架都会重新解析直链
            # 这些参数不要求全部提供， 你知道多少填多少(当然越多越好)， 剩下的交给框架去推测
            return AnimeInfo(real_url, lifetime=600, fmt="mp4", volatile=True)    # 返回 AnimeInfo 对象

    class MyVideoProxy(StreamProxy):
        """
        本类用于实现视频流量的代理， 下面的方法按需重写

        框架默认的实现可以应付大多数情况， 如果碰到一些稀奇古怪的情况， 你可能通过重写下面的某些方法
        通常 mp4 视频需要绕过防盗链， 重写 set_proxy_headers 方法即可
        许多 APP 会将 hls(m3u8) 视频片段隐藏到图片中， 需要重写  fix_chunk_data 方法剔除图片数据
        其它方法大都用于处理 m3u8 文本文件， 正常情况无需重写 
        """

        def set_proxy_headers(self, real_url: str) -> dict:
            """
            如果服务器存在防盗链, 需要检测 Referer 和 User-Agent， 可以尝试重写本方法
            本方法可为特定的直链设置代理 Headers
            若本方法返回空则使用默认 Headers
            若设置的 Headers 不包含 User-Agent 则随机生成一个
            """

            if "foo.bar" in real_url:
                return {"Referer": "http://www.foo.bar"}
        
        async def get_m3u8_text(self, index_url: str) -> str:
            """
            获取 index.m3u8 文件的内容, 如果该文件需要进一步处理,
            比如需要跳转一次才能得到 m3u8 的内容，
            或者接口返回的数据经过加密、压缩时, 请重写本方法以获取 m3u8 文件的真实内容

            :param index_url: index.m3u8 文件的链接
            :return: index.m3u8 的内容
            """
            return await self.read_text(index_url)
        
        def fix_m3u8_key_url(self, index_url: str, key_url: str) -> str:
            """
            修复 m3u8 密钥的链接(通常使用 AES-128 加密数据流),
            默认以 index.m3u8 同级路径补全 key 的链接,
            其它情况请重写本方法

            :param index_url: index.m3u8 的链接
            :param key_url: 密钥的链接(可能不完整)
            :return: 密钥的完整链接
            """
            if key_url.startswith("http"):
                return key_url

            path = '/'.join(index_url.split('/')[:-1])
            return path + '/' + key_url
        
        def fix_m3u8_chunk_url(self, index_url: str, chunk_url: str) -> str:
            """
            替换 m3u8 文件中数据块的链接, 通常需要补全域名,
            默认情况使用 index.m3u8 的域名补全数据块域名部分,
            其它情况请重新此方法

            :param index_url: index.m3u8 的链接
            :param chunk_url: m3u8 文件中数据块的链接(通常不完整)
            :return: 修复完成的 m3u8 文件
            """
            if chunk_url.startswith("http"):  # url 无需补全
                return chunk_url
            elif chunk_url.startswith('/'):
                return extract_domain(index_url) + chunk_url
            else:
                return extract_domain(index_url) + '/' + chunk_url
        
        def fix_chunk_data(self, url: str, chunk: bytes) -> bytes:
            """
            修复数 m3u8 数据据块, 用于解除数据混淆
            比如常见的图片隐写， 每一段视频数据存放于一张图片中， 需要剔除图片的数据
            可使用 binwalk 等工具对二进制数据进行分析， 以确定图像与视频流的边界位置

            :param url: 数据块的链接
            :param chunk: 数据块的二进制数据
            :return: 修复完成的二进制数据
            """
            return chunk
        

弹幕搜索引擎
=======================
弹幕引擎模板:

.. code-block:: python

    from api.core.danmaku import *

    class MyEngine(DanmakuSearcher):

        async def search(self, keyword: str):
            """
            实现本方法, 搜索弹幕摘要信息, 返回异步生成器
            """
            html = "keyword 对应的网页内容"
            items = ["番剧1的弹幕信息", "番剧2的弹幕信息"]
            for item in items:
                meta = DanmakuMeta()
                # 解析 item 提取下列信息
                meta.title = "番剧名称"
                meta.play_url = "播放页链接或参数"
                meta.num = 10 # 包含的集数
                yield meta  # 产生一个结果就交给上一级处理

    class MyDetailParser(DanmakuDetailParser):

        async def parse(self, play_url: str):
            """
            解析番剧对应的弹幕的播放列表
            """
            detail = DanmakuDetail()

            items = ["第1集的弹幕信息", "第2集的弹幕信息"]
            for ep in items:
                danmaku = Danmaku()
                danmaku.name = "本集视频的名字"
                danmaku.cid = "解析弹幕数据需要的参数或链接"
                detail.append(danmaku)

            return detail


    class MyDanmakuDataParser(DanmakuDataParser):

        async def parse(self, cid: str):
            """
            解析弹幕数据
            """
            result = DanmakuData()

            data = ["一条弹幕", "一条弹幕"]

            for item in data:
                result.append_bullet(
                    time=31.4, # 距离视频开头的秒数(float)
                    pos=1, # 位置参数(0右边, 1上边, 2底部)
                    color=int("ffffff", 16),  # 如果颜色是 16 进制, 先转 10 进制
                    message="弹幕内容"
                )
                # 也可以使用 append 方法添加弹幕
                result.append([123, 1, 16777215, "弹幕内容"])
            return result

漫画搜索引擎
=======================

还没开始整，再等等~~

小说搜索引擎
=======================

还没开始整，再等等~~

音乐搜索引擎
=======================

还没开始整，再等等~~