from functools import wraps
from secrets import compare_digest

from quart import abort, current_app, request


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = request.authorization
        if (
                auth is not None and
                auth.type == "basic" and
                auth.username == current_app.config["BASIC_AUTH_USERNAME"] and
                compare_digest(auth.password, current_app.config["BASIC_AUTH_PASSWORD"])
        ):
            return await func(*args, **kwargs)
        else:
            abort(401)

    return wrapper
