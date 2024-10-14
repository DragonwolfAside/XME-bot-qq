from collections.abc import Iterable
import config

class Doc():
    def __init__(self, name: str, desc: str, introduction: str) -> None:
        self.name = name
        self.desc = desc
        self.introduction = introduction

class PluginDoc(Doc):
    def __init__(self, name, desc, introduction, contents: Iterable[str], usages: Iterable[str], permissions: Iterable[Iterable[str]] = [[]], alias_list: Iterable[Iterable[str]] = [[]]) -> None:
        super().__init__(name, desc, introduction)
        self.permissions = permissions
        self.contents = contents
        self.usages = usages
        self.alias_list = alias_list

    def __str__(self) -> str:
        alias_lines = ""
        usages_lines = ('\n- ' + config.COMMAND_START[0]).join(self.usages)
        contents_lines = ''
        permissions_lines = ""
        for i, content in enumerate(self.contents):
            line_head = f'- {content.split(": ")[0]}: '
            try:
                alias_lines += f"{line_head}{', '.join(self.alias_list[i])}\n"
            except:
                alias_lines += f"{line_head}无\n"
            try:
                permissions_lines += f"{line_head}{'无' if len(self.permissions[i]) < 1 else ' & '.join(self.permissions[i])}\n"
            except:
                permissions_lines += f"{line_head}无\n"
            contents_lines += f"{content}\n"

        return rf"""
[插件] {self.name}
简介：{self.desc}
作用：{self.introduction}
内容：
{contents_lines}所有指令用法：
- {config.COMMAND_START[0]}{usages_lines}
权限/可用范围：
{permissions_lines}别名：
{alias_lines}
""".strip()

class CommandDoc(Doc):

    def __init__(self, name, desc, introduction, usage, permissions: Iterable[str]=[], alias: Iterable[str]=[]) -> None:
        super().__init__(name, desc, introduction)
        self.usage = usage
        self.alias = alias
        self.permissions = permissions

    def __str__(self) -> str:
        return rf"""
[指令] {self.name}
简介：{self.desc}
作用：{self.introduction}
用法：
- {config.COMMAND_START[0]}{self.name} {self.usage}
权限/可用范围：{'无' if len(self.permissions) < 1 else ' & '.join(self.permissions)}
别名：{'无' if len(self.alias) < 1 else ', '.join(self.alias)}
""".strip()