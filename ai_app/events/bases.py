from typing import Union
import hashlib
import abc
from pydantic import BaseModel
from ai_app.utils import InvalidEventException, Dict2Obj


class EventHeaderContent(BaseModel):
    event_id: str
    event_type: str
    create_time: str
    token: str
    app_id: str
    tenant_key: str


class EventContent(object):
    """事件回调内容 v2.0
    参考：
    https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
    Args:
        schema 2.0 事件模式(版本)
        header 事件头
        event 事件
    """

    schema: str = ''
    header: Union[dict, EventHeaderContent]
    event: Union[dict]

    def __init__(self, request, dict_data, token, encrypt_key):
        header = dict_data.get("header")
        event = dict_data.get("event")
        if header is None or event is None:
            raise InvalidEventException("request is not callback event(v2)")
        self.__request = request
        self.schema = dict_data.get("schema")
        self.header = Dict2Obj(header)
        self.event = Dict2Obj(event)
        self._validate(token, encrypt_key)

    def _validate(self, token, encrypt_key):
        if self.header.token != token:
            raise InvalidEventException("invalid token")
        timestamp = self.__request.headers.get("X-Lark-Request-Timestamp")
        nonce = self.__request.headers.get("X-Lark-Request-Nonce")
        signature = self.__request.headers.get("X-Lark-Signature")
        body = self.__request.body
        bytes_b1 = (timestamp + nonce + encrypt_key).encode("utf-8")
        bytes_b = bytes_b1 + body
        h = hashlib.sha256(bytes_b)
        if signature != h.hexdigest():
            raise InvalidEventException("invalid signature in event")

    @abc.abstractmethod
    def event_type(self):
        return self.header.event_type
