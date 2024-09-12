import json
import typing as t

from ai_app.events.bot import *
from ai_app.settings import FEISHU_V2_SDK_CONFIGS
from ai_app.utils import InvalidEventException
from ai_app.apis.decrypt import AESCipher


class EventManager(object):
    event_callback_map = dict()
    event_type_map = dict()
    _event_list = [MessageReceiveEvent, UrlVerificationEvent, MessageReadEvent, MessageCradEvent]

    def __init__(self):
        for event in EventManager._event_list:
            EventManager.event_type_map[event.event_type()] = event

    def register(self, event_type: str) -> t.Callable:
        def decorator(f: t.Callable) -> t.Callable:
            self.register_handler_with_event_type(event_type=event_type, handler=f)
            return f

        return decorator

    @staticmethod
    def register_handler_with_event_type(event_type, handler):
        EventManager.event_callback_map[event_type] = handler

    @staticmethod
    def get_handler_with_event(request):
        token = FEISHU_V2_SDK_CONFIGS['FEISHU_VERIFY_TOKEN']
        encrypt_key = FEISHU_V2_SDK_CONFIGS['FEISHU_ENCRYPT_KEY']
        dict_data = json.loads(request.body)
        # print('原始数据',dict_data)
        dict_data = EventManager._decrypt_data(encrypt_key, dict_data)
        # print('事件解密后dict_data:', dict_data)
        callback_type = dict_data.get("type")
        if callback_type == None:
            callback_type = dict_data.get("header").get("type")
        # only verification data has callback_type, else is event
        if callback_type == "url_verification":
            if dict_data.get('token') != token:
                raise Exception("VERIFICATION_TOKEN is invalid")
            event = UrlVerificationEvent(dict_data)
            return EventManager.event_callback_map.get(event.event_type()), event

        # only handle event v2
        schema = dict_data.get("schema")
        if schema is None:
            raise InvalidEventException("request is not callback event(v2)")

        # get event_type
        event_type = dict_data.get("header").get("event_type")
        # build event
        event = EventManager.event_type_map.get(event_type)(request, dict_data, token, encrypt_key)
        # get handler
        print(EventManager.event_callback_map.get(event_type))
        # print(event)
        return EventManager.event_callback_map.get(event_type), event

    @staticmethod
    def _decrypt_data(encrypt_key, data):
        encrypt_data = data.get("encrypt")
        if encrypt_key == "" and encrypt_data is None:
            # data haven't been encrypted
            return data
        if encrypt_key == "":
            raise Exception("ENCRYPT_KEY is necessary")
        cipher = AESCipher(encrypt_key)
        # print("明文:\n{}".format(cipher.decrypt_string(encrypt_data)))
        return json.loads(cipher.decrypt_string(encrypt_data))