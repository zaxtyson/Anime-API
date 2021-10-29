import logging

__all__ = ["logger"]

# 调试日志设置
logger = logging.getLogger('anime')
logger.setLevel(logging.DEBUG)
