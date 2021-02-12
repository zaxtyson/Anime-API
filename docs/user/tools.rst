.. _tools:

========================
网页处理工具
========================

HEAD/GET/POST
=========================

引擎模板中所以的类, 都继承自 `HtmlParseHelper` , 它封装了不少工具,
可以帮助你处理网页。当然，也提供了基本的请求 `HEAD` / `GET` / `POST` 方法,
这些方法来自 `aiohttp` 库的 `ClientSession` 。

`HtmlParseHelper` 类提供了下面 3 个成员函数：

- async def head(self, url: str, params: dict = None, \*\*kwargs) -> Optional[ClientResponse]

- async def get(self, url: str, params: dict = None, \*\*kwargs) -> Optional[ClientResponse]

- async def post(self, url: str, data: dict = None, \*\*kwargs) -> Optional[ClientResponse]

参数见 `aiohttp 库的文档 <https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request>`_

为了复用 `ClientSession` 内部的连接池，每一个类内部创建了一个 Session 对象，
在请求发出前会自动完成一次初始化，并且捕获了处理过程中可能出现的异常。
如果未设置 Headers, 或者 Headers 中缺少 User-Agent,
将自动为每一个请求设置随机的 User-Agent，默认超时被设置为 `ClientTimeout(total=30, sock_connect=5)`。
如果请求过程中出现异常，这些方法将返回 `None`，所以在使用 Response 之前，最好检查一下它是否存在。

每一个请求的参数和响应的信息都记录在日志文件中，如果有问题，可以去 `api/logs/` 下查看。
(控制台的日志等级为 `INFO`, 日志文件为 `DEBUG`)

需要注意的一个地方是，许多网页返回的 JSON 并不规范，在使用 ClientResponse 对象的 `.json()` 方法时可能出现问题，
最好加上参数 `content_type=None`。

.. code-block:: python

        ...
        resp = await self.get("http://foo.bar")
        if not resp or resp.status != 200:
            return ""
        data = await resp.json(content_type=None)

XPath
===================

XPath 是提取网页数据的利器，当然 `HtmlParseHelper` 也封装了这个功能，它来自 `lxml` 库。

关于 XPath 的语法，参见 `w3school <https://www.w3school.com.cn/xpath/index.asp>`_ ，
lxml的文档参见 `lxml.de <https://lxml.de/tutorial.html>`_

`HtmlParseHelper` 提供了下面的静态成员函数:

- def xpath(html: str, xpath: str) -> Optional[etree.Element]

同样的，它捕获了处理中可能发生的异常，如果出错，返回 `None`，错误详情见日志。

.. code-block:: python

    html = """
        <div class="container">
            <img src="http://foo.bar.1"/>
            <img src="http://foo.bar.2"/>
        </div>
    """
    result = HtmlParseHelper.xpath(html, "//div[@class='container']/img")
    if not result:
        print("not result")
    print(f"Elements count: {len(result)}")
    for item in result:
        url = item.xpath("@src")[0]
        print(url)

.. code-block:: bash

    Elements count: 2
    http://foo.bar.1
    http://foo.bar.2

并行处理
==========================
很多时候我们希望能并行解析很多网页，当然 `HtmlParseHelper` 提供了相关的功能。

下面两个静态成员函数用于处理并行任务，使用过多线/进程库的伙计可能对 `as_completed` 这个名字很熟悉，
没错，还是熟悉的味道，不过任务类型不再是函数，而是协程(Coroutine)对象。它返回一个迭代器，
每当提交的并行任务中有一个完成了，它立刻返回这个任务的结果。

- async def as_completed(tasks: Iterable[Task]) -> AsyncIterator[T]
- async def as_iter_completed(tasks: Iterable[IterTask]) -> AsyncIterator[T]

那么，下面的 `as_iter_completed` 又是什么鬼?

答：他们两个的参数不一样。`as_completed` 接受一个协程列表(可迭代的对象均可),
协程任务返回的结果类型为 `T` , 函数返回 `T` 的异步生成器。
而 `as_iter_completed` 接受的协程任务返回的结果为 `Iterable[T]` ,
函数返回也是 `T` 的异步生成器, 自动对结果进行了迭代，并行提取网页数据的时候，我们需要用到它。

这是 `as_completed` 的例子:

.. code-block:: python

    async def worker():
        data = [1, 2, 3]
        return data


    async def test():
        tasks = [worker(), worker(), worker()]
        async for item in HtmlParseHelper.as_completed(tasks):
            print(item, end=' ')


    asyncio.run(test())

.. code-block:: bash

    [1, 2, 3] [1, 2, 3] [1, 2, 3]

来看看 `as_iter_completed` 的效果:

.. code-block:: python

    async def worker():
        data = [1, 2, 3]
        return data


    async def test():
        tasks = [worker(), worker(), worker()]
        async for item in HtmlParseHelper.as_iter_completed(tasks):
            print(item, end=' ')


    asyncio.run(test())

.. code-block:: bash

    1 2 3 1 2 3 1 2 3


繁简转换
=========================
用于繁体中文和简体中文的转换的小工具，由 `zhconv` 库提供支持。

有时候我们抓取的网站并非大陆网站，这个时候需要将关键词转化为繁体，
将处理结果转换为简体。

.. code-block:: python

    from api.utils.tool import *

    if __name__ == '__main__':
        print(convert_to_tw("进击的巨人"))
        print(convert_to_zh("從零開始的異世界"))

.. code-block:: bash

    進擊的巨人
    从零开始的异世界

其它工具
==========================
对 MD5 和 BASE64 的简单封装，方便使用。

.. code-block:: python

    from api.utils.tool import *

    if __name__ == '__main__':
        print(md5("进击的巨人"))
        print(b64encode("從零開始的異世界"))

.. code-block:: bash

    d54146a0ddfdbc16ccfd28d7bdf74806
    5b6e6Zu26ZaL5aeL55qE55Ww5LiW55WM