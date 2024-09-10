from ai_app.feishu import event_manager
# Create your views here.

def event_process(request):
    """
    与飞书事件挂载
    """
    event_handler, event = event_manager.get_handler_with_event(request)
    return event_handler(event)

