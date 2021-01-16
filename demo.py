from api.router import Router


if __name__ == '__main__':
    rt = Router()
    rt.listen("127.0.0.1", port=6001, ws_port=6002)
    # rt.set_domain("example.com")      # 如果在服务器上使用
    # rt.enable_debug()                 # 启用 Flask 调试
    rt.run()
