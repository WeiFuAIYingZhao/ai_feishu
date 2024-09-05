# -*- coding: utf-8 -*-
from .bases import EventContent
from ai_app.utils import Dict2Obj

"""飞书消息和群组事件

https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/introduction
"""


class UrlVerificationEvent(EventContent):
    """
    事件类型：应用首次验证——请求地址配置
    飞书文档地址：https://open.feishu.cn/apps/cli_a27a016dd6fbd013/event
    """

    def __init__(self, dict_data):
        # event check and init
        self.event = Dict2Obj(dict_data)

    @staticmethod
    def event_type():
        return "url_verification"


class MessageReceiveEvent(EventContent):
    """
    事件类型：接收消息
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
    """

    @staticmethod
    def event_type():
        return "im.message.receive_v1"


class MessageReadEvent(EventContent):
    """
    事件类型：已读消息
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/message_read
    """

    @staticmethod
    def event_type():
        return "im.message.message_read_v1"


class AddBotEvent(EventContent):
    """
    事件类型：机器人进群
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat-member-bot/events/added
    """

    @staticmethod
    def event_type():
        return "im.chat.member.bot.added_v1"


class RemoveBotEvent(EventContent):
    """
    事件类型：机器人被移出群
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chat-member-bot/events/deleted
    """

    @staticmethod
    def event_type():
        return "im.chat.member.bot.deleted_v1"

class MessageCradEvent(EventContent):
    """
    事件类型：接收卡片消息
    飞书文档地址：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
    """

    @staticmethod
    def event_type():
        return "card.action.trigger"
