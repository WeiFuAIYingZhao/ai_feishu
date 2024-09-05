import logging
from ai_app.template_ai.crad_base import set_settings, set_que_comfy
from ai_app.client import FeishuClientURL
from celery import shared_task
from ai_app import settings
from ai_app.ComfyUI import Comfy_api

log = logging.getLogger('django')

# 加载Comfy配置信息
Comfy_set = settings.COMFYUI_V1
'''
所有异步实现方法
'''


@shared_task
def queue_pull(open_id, updata, set_or_updata=True, token=None):
    que = Comfy_api.get_queue()  # 获取队列数
    if que > 2:
        queue_json = set_que_comfy('目前等待任务数: %s 喝杯咖啡一会就好 ^_^ ' % que, updata)
    else:
        queue_json = set_que_comfy('目前等待任务数: %s 稍等一下马上就好 ^_^ ' % que, updata)
    log.info('<-----------队列信息:------->%s' % que)
    # 发送队列数
    fs_client = FeishuClientURL()
    if set_or_updata == True:
        que_msg = fs_client.send_crad_msg(msg=queue_json, receive_id_type='open_id', open_id=open_id,
                                          msg_type='interactive')
    else:
        que_msg = fs_client.updata_crad_msg(open_id=open_id, msg=queue_json, token=token)
    log.info('<-----------队列发送状态--- %s', que_msg)
    return que_msg


@shared_task
def updata_crad_task(test, open_id, token, comfy_id):
    '''
       更新卡片异步方法
    '''
    log.info('<-------------------队列发送--------->')
    log.info('<-----------Updating Crad Task----------->')
    fs_client = FeishuClientURL()
    # 生成并上传图片
    put_queue = Comfy_api.generate_clip(test, 1, 'workflow_api.json', comfy_id)
    updata_images = fs_client.up_image_data(image=put_queue, image_type='message')
    msg1 = set_settings(updata_images, test, True)
    # 发送卡片
    updata_msg = fs_client.updata_crad_msg(open_id=open_id, msg=msg1, token=token)
    log.info('<-----------updata_msg: %s ', updata_msg)
    return 'ok'


@shared_task()
def up_msg_task(receive_id, test, comfy_id):
    '''
        发送卡片异步方法
    '''
    log.info('<-----------Up msg Task----------->')
    put_queue = Comfy_api.generate_clip(test, 1, 'workflow_api.json', comfy_id)
    fs_client = FeishuClientURL()
    updata_images = fs_client.up_image_data(image=put_queue, image_type='message')
    log.info(updata_images)
    msg = set_settings(updata_images, test, False)
    res = fs_client.send_crad_msg(msg=msg, receive_id_type='open_id', open_id=receive_id,
                                  msg_type='interactive')  # interactive
    log.info('<-----------updata_msg: %s ', res)
    return 'ok'


def  url_crad_data():
    import json
    import requests

    url = "https://open.feishu.cn/open-apis/interactive/v1/card/update"
    payload = json.dumps({
        # "content": "{\"elements\": [{\"tag\": \"img\", \"img_key\": \"img_v3_02eb_8119c139-00e2-4039-8e2a-76afb37de7ag\"}]}"
        "token":"c-58cff1129b126f81e7307c121c564da41faface0",
        "card":{"open_ids":["ou_c94d3930355346d5ff6c6e0bfd31d8bf"],
                'elements': [{'tag': 'img', 'img_key': 'img_v3_02eb_8119c139-00e2-4039-8e2a-76afb37de7ag'}]}
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer t-g104939CQ2J2ITHJVQ5WFJBRWN5AYL3AS3FDOADS'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    a = json.loads(response.text)
    print(a.get("code"))

if __name__ == '__main__':
    url_crad_data()