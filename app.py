from api.router import app, loop
from global_config import host, port

if __name__ == '__main__':
    app.run(host, port, debug=False, loop=loop)
