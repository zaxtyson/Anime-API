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
因为你无法预料目标网站使用了何种手段阻止你的抓取，不知道它将某些关键参数藏到了哪里，
即便已经接近成功，它仍可能返回一些古怪的数据再次使你迷惑。
这里有不少的坑，我个人的一些经验总结在了
:ref:`爬虫技巧 <skills>` 一栏，
如果遇到问题，可以看看，说不定能得到启发。

OK，说了一大堆，现在我们终于要开始了！

现在，你盯上了一个网站，觉得它的资源很不错，可是广告满天飞，
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
            items = ["剧集1的信息", "剧集2的信息", "剧集3的信息"]
            for item in items:
                meta = AnimeMeta()
                meta.title = "番剧名称"
                meta.category = "分类"
                meta.desc = "简介"
                meta.cover_url = "封面图 URL"
                meta.detail_url = "详情页链接或参数"
                yield meta  # 产生一个结果就交给上一级处理


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
                pl.name = "播放列表名"
                for item in playlist:
                    anime = Anime()
                    anime.name = "某一集视频的名字"
                    anime.raw_url = "视频的原始链接或者参数"
                    pl.append(anime)
                detail.append_playlist(pl)
            return detail

    class MyUrlParser(AnimeUrlParser):

        async def parse(self, raw_url: str):
            """
            实现本方法, 解析某一集视频的原始链接, 获取直链和有效期
            如果在详情页已经提取到了有效的直链, 可以不写这个类, 但通常是需要的
            """
            # raw_url 是从详情页提取的信息
            real_url = "根据 raw_url 找到的视频直链"
            return real_url # 直接返回直链是可以的

            # 如果能找到直链的有效期就更好了
            lifetime = 600 # 直链的剩余寿命, 秒
            return AnimeInfo(real_url, lifetime)    # 返回 AnimeInfo 对象

    class MyVideoProxy(StreamProxy):

        def set_proxy_headers(self, real_url: str) -> dict:
            """
            如果服务器存在防盗链, 可以尝试重写本方法, 通常是不需要写这个类的
            本为特定的直链设置代理 Headers
            若本方法返回空则使用默认 Headers
            若设置的 Headers 不包含 User-Agent 则随机生成一个
            """

            if "foo.bar" in real_url:
                return {"Referer": "http://www.foo.bar"}



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