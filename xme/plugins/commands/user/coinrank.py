from xme.plugins.commands.user import __plugin_name__
from nonebot import on_command, CommandSession
from xme.xmetools.doc_gen import CommandDoc
from xme.xmetools.command_tools import send_msg
from bisect import bisect_left
from xme.xmetools import xme_user
from xme.xmetools import text_tools
from xme.xmetools.xme_user import User, coin_name, coin_pronoun
from character import get_message


alias = ['rank', f'{coin_name}排行', 'ranking']
MAX_RANK_COUNT = 20
cmd_name = 'coinrank'
usage = {
    "name": __plugin_name__,
    "desc": get_message(__plugin_name__, cmd_name, 'desc').format(coin_name=coin_name),
    "introduction": get_message(__plugin_name__, cmd_name, 'introduction').format(coin_name=coin_name),
    "usage": f'<参数>',
    "permissions": [],
    "alias": alias
}
def rank_operation(func, rank_items):
    return func([item[1] for item in rank_items])

@on_command(cmd_name, aliases=alias, only_to_me=False)
async def _(session: CommandSession):
    sender = session.event.user_id
    message = get_message(__plugin_name__, cmd_name, 'rank_msg_prefix').format(coin_name=coin_name, coin_pronoun=coin_pronoun)
    arg = session.current_arg_text.strip().lower()
    rank_count = 10
    rank_items = xme_user.get_rank('coins')
    if arg and arg == 'avg':
        # 平均值消息
        rank_avg = rank_operation(lambda x: sum(x) / len(x), rank_items)
        message = get_message(__plugin_name__, cmd_name, 'rank_msg_avg').format(
            coin_name=coin_name,
            coin_pronoun=coin_pronoun,
            avg=int(rank_avg)
        )
        await send_msg(session, message)
        return True
    elif arg and arg == 'sum':
        # 总和消息
        rank_sum = rank_operation(lambda x: sum(x), rank_items)
        message = get_message(__plugin_name__, cmd_name, 'rank_msg_sum').format(
            coin_name=coin_name,
            coin_pronoun=coin_pronoun,
            sum=rank_sum
        )
        await send_msg(session, message)
        return True
    elif arg:
        try:
            rank_count = int(arg)
            if rank_count <= 0:
                await send_msg(session, get_message(__plugin_name__, cmd_name, 'count_too_small'))
                return False
            elif rank_count > MAX_RANK_COUNT:
                await send_msg(session, get_message(__plugin_name__, cmd_name, 'count_too_large').format(count_max=MAX_RANK_COUNT))
                return False
        except ValueError:
            await send_msg(session, get_message(__plugin_name__, cmd_name, 'invalid_arg'))
            return False
    # rank_items = rank.items()[:10]
    print(rank_items)
    rank_items_short = rank_items[:rank_count]
    print("查询中")
    u_names = {k: v for k, v in [(id, (await session.bot.api.get_stranger_info(user_id=id))['nickname']) for id, _ in rank_items_short]}
    # print(u_names)
    for i, (id, v) in enumerate(rank_items_short):
        # u_name = (await session.bot.api.get_stranger_info(user_id=id))['nickname']
        nickname = u_names[id]
        message += '\n' + get_message(__plugin_name__, cmd_name, 'ranking_row').format(
            rank=i + 1,
            nickname=nickname,
            coins_count=v,
            coin_pronoun=coin_pronoun,
            coin_name=coin_name,
            spacing=" " * text_tools.calc_spacing(list(u_names.values()), nickname, 2)
        )
    # 关于发送者的金币数超过了多少人
    sender_coins_count = None
    sender_index = None
    for index, item in enumerate(rank_items):
        # print(item[0], sender)
        if int(item[0]) != sender: continue
        print("匹配到了")
        sender_coins_count = item[1]
        sender_index = index
    # sender_coins_count = rank.get(sender, None)
    # print(sender_coins_count)
    if sender_coins_count:
        # rank_ratio = rank_operation(lambda x: (bisect_left(x, rank_items[sender_index][1])), rank_items)
        rank_ratio = max(len(rank_items[sender_index:]) - 1, 0) / len(rank_items) * 100
        message += '\n' + get_message(__plugin_name__, cmd_name, 'ranking_suffix').format(
            count=sender_coins_count,
            rank_ratio=f"{rank_ratio:.2f}",
            coin_pronoun=coin_pronoun,
            coin_name=coin_name
        )
    await send_msg(session, message)
    return True