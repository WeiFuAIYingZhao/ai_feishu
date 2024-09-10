from ai_app import settings
import json, requests, logging
from enum import Enum
from requests_toolbelt import MultipartEncoder


class ImageType(str, Enum):
    MESSAGE = "message"
    AVATAR = "avatar"

    def __str__(self):
        return self.value


# 飞书python-Request调用方法
class FeishuClientURL:
    key = settings.FEISHU_V2_SDK_CONFIGS

    def __init__(self):
        # 获取飞书授权key
        self.app_id = self.key['FEISHU_APP_ID']
        self.APP_SECRET = self.key['FEISHU_APP_SECRET']
        self.VERIFY_TOKEN = self.key['FEISHU_VERIFY_TOKEN']
        self.ENCRYPT_KEY = self.key['FEISHU_ENCRYPT_KEY']
        self.URL = "https://open.feishu.cn/open-apis/"
        self.log = logging.getLogger('FeiShu')

    def get_tenant_access_token(self):
        API = self.URL + "auth/v3/tenant_access_token/internal"
        Method = "POST"
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.APP_SECRET
        })
        response = json.loads(requests.request(Method, API, headers=headers, data=payload).text)
        if response.get('code') == 0:
            token = 'Bearer %s' % response.get('tenant_access_token')
            return token
        else:
            self.log.error(f"Failed to get tenant access token: {response}")
            return

    def send_crad_msg(self, open_id, msg, receive_id_type, msg_type, message_id):
        tenant_access_token = self.get_tenant_access_token()
        if message_id == False:
            Method = "POST"
            API = self.URL + "im/v1/messages"
        else:
            API = self.URL + "im/v1/messages/%s" % message_id
            Method = "PATCH"
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': tenant_access_token
        }
        params = {"receive_id_type": receive_id_type}
        req = {
            "receive_id": open_id,  # chat id
            "msg_type": msg_type,
            "content": msg
        }
        payload = json.dumps(req)
        # print(payload)
        response = json.loads(requests.request(Method, API, params=params, headers=headers, data=payload).text)
        if response.get('code') == 0:
            return response.get('data').get('message_id')
        else:
            self.log.error(f"Failed to send crad msg: {response}")
            return

    def updata_crad_msg(self, open_id, msg, token):
        tenant_access_token = self.get_tenant_access_token()
        API = self.URL + "interactive/v1/card/update"
        Method = "POST"
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': tenant_access_token
        }
        # print(msg)
        msg = json.loads(msg)
        payload = json.dumps({
            "token": token,
            "card": {"open_ids": [open_id],
                     'elements': msg["elements"]}
        })
        response = json.loads(requests.request(Method, API, headers=headers, data=payload).text)
        if response.get('code') == 0:
            return response.get('msg')
        else:
            self.log.error(f"Failed to up data crad : {response}")
            return

    def up_image_data(self, image, image_type):
        tenant_access_token = self.get_tenant_access_token()
        API = self.URL + "im/v1/images"
        Method = "POST"
        form = {'image_type': image_type,
                'image': (open(image, 'rb'))}
        multi_form = MultipartEncoder(form)
        headers = {
            'Content-Type': multi_form.content_type,
            'Authorization': tenant_access_token
        }
        response = json.loads(requests.request(Method, API, headers=headers, data=multi_form).text)
        if response.get('code') == 0:
            return response.get('data').get("image_key")
        else:
            self.log.error(f"Failed to up data image : {response}")
            return
