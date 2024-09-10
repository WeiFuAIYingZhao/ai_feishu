import json
# 飞书卡片json设置

def set_settings(img_key, prompt, updata):
    # 空卡片列表
    elements = []
    # 飞书卡片图片配置
    elements.append(
    {
        "tag": "img",
        "img_key": img_key,
        "alt": {
            "tag": "plain_text",
            "content": ""
        },
        "mode": "fit_horizontal",
        "preview": True
        }
    )
    # 飞书卡片按钮配置
    elements.append(
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": "试试手气 - AI润色 - 30秒"
                    },
                    "type": "primary",
                    "value": {
                        "type": "reload",
                        "prompt": prompt,
                        "image_data": img_key,
                    }
                }
            ]
        }
    )

    #片段是否是更新卡片
    if updata == False:
        # 添加卡片头信息
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
    else:
        result = {"elements": elements}
    msg = json.dumps(result)
    return msg

def set_que_comfy(prompt, updata):
    # 空卡片列表
    elements = []
    # 飞书卡片图片配置
    elements.append(
        {
            "tag": "div",
            "text": {
                "content": prompt,
                "tag": "plain_text"
            }
        }
    )
    # 是否是更新卡片
    if updata == False:
        # 添加卡片头信息
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
    else:
        result = {"elements": elements}
    msg = json.dumps(result)
    return msg


def set_up_crad(prompt, content, updata, img_key):
    # 空卡片列表
    elements = []
    # 飞书卡片图片配置
    elements.append(
        {
            "tag": "img",
            "img_key": img_key,
            "alt": {
                "tag": "plain_text",
                "content": ""
            },
            "mode": "fit_horizontal",
            "preview": True
        }
    )
    # 飞书卡片按钮配置
    elements.append(
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": content
                    },
                    "type": "primary",
                    "disabled": True,
                    "disabled_tips": {
                        "tag": "plain_text",
                        "content": "已经提交"
                    },
                    "value": {
                        "type": "reload",
                        "prompt": prompt,
                        "image_data": img_key,
                    }
                }
            ]
        }
    )
    # 是否是更新卡片
    if updata == False:
        # 添加卡片头信息
        result = {"config": {"wide_screen_mode": True}, "elements": elements}
    else:
        result = {"elements": elements}
    msg = json.dumps(result)
    return msg

if __name__ == '__main__':
    print(set_que_comfy('11111111',True))


