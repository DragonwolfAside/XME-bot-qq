from nonebot import on_websocket_connect
import aiocqhttp
import xme.xmetools.color_manage as c
import xme.xmetools.num_tools as n
import nonebot
import config
import bot_variables as var

@on_websocket_connect
async def connect(event: aiocqhttp.Event):
    bot = nonebot.get_bot()
    print(c.gradient_text("#dda3f8","#66afff" ,text=f"XME-bot 准备好啦~"))
    if not n.is_prime(var.currentpid):
        message = f"[DEBUG] XME-bot 准备好啦~"
        if not config.DEBUG: return
    else:
        message = f"我的 PID 是质数诶~ ({var.currentpid})"
    for group_id in config.GROUPS_WHITELIST:
        await bot.api.send_group_msg(group_id=group_id, message=message)