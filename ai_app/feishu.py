from django.http import JsonResponse
# 飞书的SDK
from ai_app.client import FeishuClientURL
from ai_app.events import UrlVerificationEvent, MessageReadEvent
from ai_app.apis.event import EventManager
from ai_app.tasks import updata_crad_task, up_msg_task, queue_pull
import logging
import uuid

log = logging.getLogger('django')
event_manager = EventManager()


# 处理飞书首次事件配置
@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    return JsonResponse({"challenge": req_data.event.challenge})


# 处理飞书事件监听
@event_manager.register("im.message.receive_v1")
def message_get_event(req_data: MessageReadEvent):
    comfy_id = str(uuid.uuid4())
    receive_id = req_data.event.get('sender').get('sender_id').get('open_id')
    test = req_data.event.get('message').get('content')
    queue_pull.delay(open_id=receive_id, updata=False)
    up_msg_task.delay(receive_id=receive_id, test=test, comfy_id=comfy_id)
    return JsonResponse({"message": "succeed"})

# 处理飞书已读事件监听
@event_manager.register("im.message.message_read_v1")
def message_read_event_handler(req_data: MessageReadEvent):
    print('监控到消息已读')
    return JsonResponse({"message": "OK"})

# 处理飞书卡片回传事件监听
@event_manager.register("card.action.trigger")
def message_card_event_handler(req_data: MessageReadEvent):
    comfy_id = str(uuid.uuid4())
    receive_id = req_data.event.get('operator').get('open_id')
    open_message_id = req_data.event.get('context').get('open_message_id')
    log.info('事件处理ID：%s', open_message_id)
    log.info('事件内容：%s', req_data.event)
    msg = req_data.event.get('action').get('value').get('prompt')
    token = req_data.event.get('token')
    queue_pull.delay(receive_id, True, False, token)
    updata_crad_task.delay(test=msg, open_id=receive_id, token=token, comfy_id=comfy_id)
    return JsonResponse({"message": "succeed"})

def test():
    fs_client = FeishuClientURL()
    a = fs_client.get_tenant_access_token()
    # add.delay(fs_client)
    # aaa.delay(123,222)
    print(a)
if __name__ == '__main__':
    test()
    print(2222222)