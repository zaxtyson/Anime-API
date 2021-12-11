from quart import Blueprint, Response, request, jsonify

from api import root_path, config, agent
from api.utils.storage import Storage

mod = Blueprint("system", __name__, url_prefix="/system")
storage = Storage()


@mod.route("/logs")
async def logs():
    """获取运行日志"""
    file = root_path + "/logs/api.log"
    with open(file, encoding="utf-8") as f:
        text = f.read()
    return Response(text, mimetype="text/plain")


@mod.route("/version")
async def version():
    """获取版本信息"""
    return jsonify(config.get_version())


@mod.route("/clear")
async def clear():
    """清空 API 的临时缓存数据"""
    mem_free = agent.cache_clear()
    return jsonify({"clear": "success", "free": mem_free})


@mod.route("/modules", methods=["GET", "POST", "OPTIONS"])
async def modules():
    if request.method == "GET":
        return jsonify(config.get_modules_status())
    elif request.method == "POST":
        options = await request.json
        ret = {}
        for option in options:
            module = option.get("module")
            enable = option.get("enable")
            if not module:
                continue
            ok = agent.change_module_state(module, enable)
            ret[module] = "success" if ok else "failed"
        return jsonify(ret)
    elif request.method == "OPTIONS":
        return Response("")


@mod.route("/storage", methods=["POST", "OPTIONS"])
async def web_storage():
    """给前端持久化配置用"""
    if request.method == "OPTIONS":
        return Response("")
    if request.method == "POST":
        payload = await request.json
        if not payload:
            return jsonify({"msg": "payload format error"})

        action: str = payload.get("action", "")
        key: str = payload.get("key", "")
        data: str = payload.get("data", "")

        if not key:
            return jsonify({"msg": "key is invalid"})

        if action.lower() == "get":
            return jsonify({
                "msg": "ok",
                "key": key,
                "data": storage.get(key)
            })
        elif action.lower() == "set":
            storage.set(key, data)
            return jsonify({
                "msg": "ok",
                "key": key,
                "data": data,
            })
        elif action.lower() == "del":
            return jsonify({
                "msg": "ok" if storage.delete(key) else "no data binds this key",
                "key": key
            })
        else:
            return jsonify({
                "msg": "action is not supported",
                "action": action
            })
