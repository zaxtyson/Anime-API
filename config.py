"""
全局配置文件
"""
import os

# 绑定的 IP, 服务器端请使用公网 IP
# 如果不确定可以使用 0.0.0.0
env_addr = os.environ.get("LISTEN_ADDR", "")
host = env_addr or "127.0.0.1"

# API 服务的端口
env_port = os.environ.get("LISTEN_PORT", "")
env_port = int(env_port) if env_port.isdigit() else None
port = env_port or 6001

# 设置资源路径的域名部分, 端口使用 port
# 如: http://www.foo.bar
env_domain = os.environ.get("ASSET_DOMAIN", "")
domain = env_domain or "http://localhost"

# 设置资源路径的前缀, 结尾不加 "/"
# 反向代理时使用, 该选项会覆盖 domain 的设置
# 如: http://www.foo.bar/anime-api
env_prefix = os.environ.get("PROXY_PREFIX", "")
proxy_prefix = env_prefix or ""
