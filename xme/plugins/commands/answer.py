from nonebot import on_command, CommandSession
from xme.xmetools.doc_gen import CommandDoc
import json
import requests

alias = ['答案之书', 'ans']
__plugin_name__ = 'answer'
__plugin_usage__ = str(CommandDoc(
    name=__plugin_name__,
    desc='答案之书',
    introduction='随机翻开答案之书的一页，并且返回内容\n"心中默念你的问题，将会得到你的答案。"',
    usage=f'',
    permissions=[],
    alias=alias
))

@on_command(__plugin_name__, aliases=alias, only_to_me=False)
async def _(session: CommandSession):
    message = "呜呜，出现未知错误"
    try:
        ans_json = json.loads(requests.get('https://api.andeer.top/API/answer.php').text)
        if ans_json['code'] != 200:
            message = "呜呜，答案获取失败"
        else:
            message = f"[CQ:at,qq={session.event.user_id}]\n答案之书：\n\"{ans_json['data']['zh']}\""
    except Exception as ex:
        print(ex)
    finally:
        await session.send(message)