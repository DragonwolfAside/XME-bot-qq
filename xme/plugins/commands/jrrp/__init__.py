from anyio import sleep
# from itsdangerous import base64_encode
import nonebot
import random
from nonebot import on_command, CommandSession
from xme.xmetools.date_tools import curr_days
# from xme.plugins.commands.jrrp.luck_algorithm import get_luck
from xme.xmetools.doc_gen import CommandDoc

alias = ["今日人品" , "luck"]
__plugin_name__ = 'jrrp'

__plugin_usage__= str(CommandDoc(
    name=__plugin_name__,
    desc='今日人品',
    introduction='返回你今天的人品值（？） [by 千枫]\n参数填写整数，正数为人品最高排名，负数为最低',
    usage=f'jrrp <群员人品值排行人数>',
    permissions=[],
    alias=alias
))

@on_command(__plugin_name__, aliases=alias, only_to_me=False)
async def jrrp(session: CommandSession):
    args = session.current_arg_text.strip()
    # print()
    qq = session.event.user_id
    if args:
        members = await jrrp_rank(session)
        try:
            count = int(args)
        except:
            await session.send(f"成员数量需要是整数哦ovo")
            return
        if count > 15 or count < -15:
            await session.send(f"指定的成员数量太多了哦uwu，范围是 -15 ~ 15")
            return
        elif count == 0:
            count = 5
            return
        message = f"这是今天人品最{'高' if count > 0 else '低'}的前 {abs(count)} 位群员排名 {'owo' if count > 0 else 'uwu'}"
        if count > 0:
            enum_list = members[:count]
        elif count < 0:
            enum_list = members[count:]
            enum_list.reverse()
        for i, member in enumerate(enum_list):
            message += f"\n{i + 1}. {member['card']} ({member['id']})：今日人品值为 {member['jrrp']}"
        await session.send(message)
        return
    # key = base64_encode("嘿嘿嘿...179....嘿嘿嘿")
    # result = get_luck(qq, key)
    # random.seed(int(str(curr_days()) + str(qq)))
    result = jrrp_gen(qq)
    content = f"[CQ:at,qq={qq}] 你的今日人品为"
    if result < 0:
        await session.send(content + f"{result}...？ xwx")
    elif result < 10:
        await session.send(content + f"....{result}？uwu")
    elif result > 100:
        await session.send(content + f"{result}.0000%！All Perfect+ owo！！")
    elif result >= 90:
        await session.send(content + f"{result}！owo！")
    else:
        await session.send(content + f"{result} ovo")

def jrrp_gen(id):
    random.seed(int(str(curr_days()) + str(id)))
    return random.randint(-1, 101)

async def jrrp_rank(session: CommandSession):
    members_full = await nonebot.get_bot().get_group_member_list(group_id=session.event.group_id)
    members = [{"id": member['user_id'], "card": member['card'] if member['card'] else member['nickname'], "jrrp": jrrp_gen(member['user_id'])} for member in members_full]
    members.sort(key=lambda x: (x['jrrp'], x['id']), reverse=True)
    return members
