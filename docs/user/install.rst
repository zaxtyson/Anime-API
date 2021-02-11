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
    python app.py


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
    host = "0.0.0.0"

    # API 服务的端口
    port = 6001

    # 绑定域名, 含协议字段不含端口号
    domain = "http://www.foo.bar"

运行服务即可

.. code-block:: bash

    python3.8 app.py

如果需要保持后台服务，可使用 nohup

.. code-block:: bash

    nohup python3.8 app.py &


浏览器打开 `ip:port` 或者 `domain:port` 就可以看到效果了

默认的配置为 `127.0.0.1:6001`