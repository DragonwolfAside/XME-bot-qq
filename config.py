from nonebot.default_config import *
import character
from datetime import timedelta

# SUPERUSERS = character.get_item('config', 'super_users', default={1795886524})
SUPERUSERS = {1795886524}
COMMAND_START = ['/', '!', '！', '.', '。']
HOST = '0.0.0.0'
PORT = 17980
DEFAULT_VALIDATION_FAILURE_EXPRESSION = character.get_message('config', 'default_validation_failure_expression')
# DEFAULT_VALIDATION_FAILURE_EXPRESSION = '发送内容格式出错啦 xwx，可以检查一下输入或问问 179 哦'
DEBUG = False
SESSION_EXPIRE_TIMEOUT = timedelta(minutes=3)
SESSION_RUN_TIMEOUT = timedelta(seconds=180)
SESSION_RUNNING_EXPRESSION = character.get_message('config', 'busy')
DEFAULT_COMMAND_PERMISSION = lambda s: s.is_groupchat

# 用户自定义 config
GROUPS_WHITELIST = [
    727949269
]
# 报时
SCHEDULER_GROUP = [
    727949269,
    913581215,
    164072032,
]

NICKNAME = character.get_item('bot_info', 'nickname', default=['XME', 'xme'])
VERSION = '0.1.3'

USER_PATH = "./data/users.json"

