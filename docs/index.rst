.. _index:

======================
Anime-API Documents
======================

Anime-API 是一个异步的资源解析框架, 基于 asyncio 和 aiohttp

用于组织各类爬虫抓取互联网上的资源, 为前端提供格式统一的接口服务

因为前期以动漫、弹幕抓取为主, 所以叫 *Anime-API*

后面会加入漫画、小说、音乐等抓取功能哦 :)

-------------------

**创建 API 服务**:

    >>> from api.router import app, loop
    >>> from global_config import host, port
    >>>
    >>> if __name__ == '__main__':
    >>>    app.run(host, port, debug=False, loop=loop)

----------------------


食用指南
============

那么，这个破玩意到底怎么用呢?

.. toctree::
   :maxdepth: 2
   
   user/disclaimer
   user/install
   user/interface
   user/extension
   user/tools
   user/skills
   user/class
