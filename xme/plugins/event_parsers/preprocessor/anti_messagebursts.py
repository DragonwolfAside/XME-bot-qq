from nonebot import NoneBot
from nonebot.plugin import PluginManager
from nonebot.message import CanceledException
from xme.xmetools import command_tools
import aiocqhttp
from character import get_message
from nonebot import message_preprocessor
from nonebot import NoneBot
import time
import config
# import asyncio
last_messages = {
    "refresh_time": 0
}


@message_preprocessor
async def anti_bursts_handler(bot: NoneBot, event: aiocqhttp.Event, plugin_manager: PluginManager):
    global last_messages
    # recalls = json_tools.read_from_path('./recalls.json')['recalls']
    MSG_COUNT_THRESHOLD = 3
    SEC_AVG_MSGS = 0.8
    try:
        key = f"{event['user_id']}{event['group_id']}"
    except:
        return
    if event['user_id'] == event.self_id:
        return
    message = x if (x:=event['raw_message'].strip()) else event['raw_message']
    if message.strip():
        is_cmd = command_tools.get_cmd_by_alias(message.split(" ")[0])
    else:
        is_cmd = False
    # 如果是指令只保留指令名部分
    if is_cmd:
        message = message.split(" ")[0]
        message = message[1:] if message[0] in config.COMMAND_START else message
    if time.time() - last_messages['refresh_time'] > (SEC_AVG_MSGS * MSG_COUNT_THRESHOLD * 2) and last_messages['refresh_time'] > 0:
        # print(last_messages)
        print(f"清除以上缓存")
        last_messages = {
            "refresh_time": time.time()
        }
    elif last_messages['refresh_time'] <= 0:
        last_messages['refresh_time'] = time.time()
    last_messages.setdefault(key, {}).setdefault(message, {})
    last_messages[key][message].setdefault("count", 0)
    if not last_messages[key][message].get("start_time", False):
        # print(f"记录新语句: {message}")
        last_messages[key][message]["start_time"] = time.time()
    last_messages[key][message]['count'] += 1
    if not last_messages[key][message].get("banned", False):
        last_messages[key][message]["banned"] = False
    # print(last_messages)

    if last_messages[key][message]['count'] >= MSG_COUNT_THRESHOLD:
        # 刷屏了 禁言
        rate = 2 if is_cmd else 1
        # 如果在 x 秒内发的消息超过这么多则算刷屏
        time_period = time.time() - last_messages[key][message]["start_time"]
        print(f'在 {time_period} 秒发了 {last_messages[key][message]["count"]} 条消息 {message}，{"是" if is_cmd else "不是"}指令，平均每秒发送了 {time_period / last_messages[key][message]["count"]} 条消息\n刷屏限制为每秒 {SEC_AVG_MSGS / rate} 条消息')
        if time_period > (SEC_AVG_MSGS * rate * last_messages[key][message]['count']): return
        if last_messages[key][message]['count'] < MSG_COUNT_THRESHOLD * 4:
            last_messages['refresh_time'] = time.time()
        if not last_messages[key][message]["banned"]:
            # 禁言 / 提醒
            print(f"消息 \"{message}\" 刷屏了")
            last_messages[key][message]["banned"] = True
            if event['group_id'] in config.GROUPS_WHITELIST and time_period <= (SEC_AVG_MSGS * last_messages[key][message]['count']):
                print(f"尝试禁言群员")
                await bot.api.set_group_ban(group_id=event['group_id'], user_id=event['user_id'], duration=120)
            if event['group_id'] in config.GROUPS_WHITELIST or is_cmd:
                print("提醒群员")
                await bot.send_group_msg(message=get_message("event_parsers", "cmd_bursts" if is_cmd else "message_bursts"), group_id=event['group_id'])
        raise CanceledException(f"消息 \"{event.raw_message}\" 刷屏，不处理")
    return