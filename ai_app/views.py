from django.shortcuts import render
from django.http import JsonResponse
from ai_app.feishu import event_manager
# Create your views here.

def event_process(request):
    """
    与飞书事件挂载
    """
    event_handler, event = event_manager.get_handler_with_event(request)
    return event_handler(event)


# 飞书卡片回调处理
def event_card(request):
    print('进入飞书卡片回调处理')
    event_handler, event = event_manager.get_handler_with_event(request)
    return event_handler(event)


def test(request):
    # result = aaa.delay(123, 222)
    # print(result.get())
    # print(result.__dict__)
    # print(result.successful())
    # print(result.fail())
    # print(result.ready())
    # print(result.state)
    return JsonResponse({"message": "OK"})

