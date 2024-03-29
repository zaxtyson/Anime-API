from api.router import APIRouter
from config import *

if __name__ == '__main__':
    app = APIRouter(host, port)
    app.set_domain(domain)
    app.set_proxy_host(proxy_prefix)
    app.run()
