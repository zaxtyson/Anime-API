.. _install:

======================
安装和部署
======================

当然还是先把 demo 跑起来再说

本地使用
===============

克隆仓库，安装依赖，运行即可。

注意，本项目需要使用 Python3.8+ 运行，

.. code-block:: bash

    git clone https://github.com.cnpmjs.org/zaxtyson/Anime-API.git
    pip install -r requirements.txt
    python3.8 app.py


服务器端部署
=================

服务器端部署 API 服务时，系统中可能存在多个 Python 版本，请指名具体的 Python 版本运行，
防止依赖安装到其它版本中。

.. code-block:: bash

    git clone https://github.com.cnpmjs.org/zaxtyson/Anime-API.git
    cd Anime-API
    python3.8 -m pip install -r requirements.txt

修改 `config.py`，按照提示修改 IP 和域名信息

.. code-block:: python

    # 绑定的 IP, 服务器端请使用公网 IP
    # 如果不确定可以使用 0.0.0.0
    host = "127.0.0.1"

    # API 服务的端口
    port = 6001

    # 设置资源路径的前缀, 结尾不加 "/"
    # 反向代理或者需要设置域名时使用
    # 如: http://www.foo.bar/anime-api
    #     http://www.foo.bar:12345/anime-api
    root_prefix = ""

    # 强制代理图片资源， 服务器部署时遇到图片跨域请启用此项
    enforce_proxy_images = True

    # 强制代理全部视频流量， 通常使用默认策略即可
    enforce_proxy_videos = False

    # 缓存策略, 秒
    cache_expire_policy = {
        "anime": 60 * 30,  # 视频详情和播放列表缓存
        "bangumi": 60 * 60 * 1,  # 番剧更新数据
        "danmaku": 60 * 60 * 12  # 弹幕库搜索结果及弹幕数据
    }

运行服务即可

.. code-block:: bash

    python3.8 app.py

如果需要保持后台服务，可使用 nohup

.. code-block:: bash

    nohup python3.8 app.py &


浏览器打开 `ip:port` 或者 `domain:port` 就可以看到效果了

默认的配置为 `127.0.0.1:6001`