from django.test import TestCase

# Create your tests here.
# -- utf-8 ---
# https://www.bilibili.com/read/cv33202530/
# https://www.wehelpwin.com/article/5317
import json
import websocket
import uuid
import urllib.request
import urllib.parse
import random


# 显示图片
def show_gif(fname):
    import base64
    from IPython import display
    with open(fname, 'rb') as fd:
        b64 = base64.b64encode(fd.read()).decode('ascii')
    return display.HTML(f'<img src="data:image/gif;base64,{b64}" />')


# 向服务器队列发送提示词
def queue_prompt(textPrompt):
    p = {"prompt": textPrompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


# 获取生成图片
def get_image(fileName, subFolder, folder_type):
    data = {"filename": fileName, "subfolder": subFolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    print('-----------------', "http://{}/view?{}".format(server_address, url_values))
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


# 获取历史记录
def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


# 获取图片，监听WebSocket消息
def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    print('prompt: {}'.format(prompt))
    print('prompt_id:{}'.format(prompt_id))
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    print('执行完成')
                    break
        else:
            continue
    history = get_history(prompt_id)[prompt_id]
    print(history)
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            # 图片分支
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                    output_images[node_id] = images_output
            # 视频分支
            if 'videos' in node_output:
                videos_output = []
                for video in node_output['videos']:
                    video_data = get_image(video['filename'], video['subfolder'], video['type'])
                    videos_output.append(video_data)
                    output_images[node_id] = videos_output
    # print('获取图片完成：{}'.format(output_images))
    return output_images


# 解析comfyUI 工作流并获取图片
def parse_worflow(ws, prompt, seed, workflowfile):
    workflowfile = workflowfile
    print('workflowfile:{}'.format(workflowfile))
    with open(workflowfile, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
        prompt_data = json.load(workflow_api_txt2gif_file)
        # 设置文本提示
        prompt_data["6"]["inputs"]["text"] = prompt
        # 设置随机数
        prompt_data["3"]["inputs"]["seed"] = seed
        return get_images(ws, prompt_data)


# 生成图像
def generate_clip(prompt, seed, workflowfile, idx):
    print('seed:' + str(seed))
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = parse_worflow(ws, prompt, seed, workflowfile)
    for node_id in images:
        for image_data in images[node_id]:
            from datetime import datetime
            # 获取当前时间，并格式化为 YYYYMMDDHHMMSS 的格式
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # 使用格式化的时间戳在文件名中
            GIF_LOCATION = "{}/{}_{}_{}.png".format('D:/django-env/ai_feishu/ai_app/output', idx, seed, timestamp)
            print('GIF_LOCATION:' + GIF_LOCATION)
            with open(GIF_LOCATION, "wb") as binary_file:
                # 写入二进制文件
                binary_file.write(image_data)
                print("{} DONE!!!".format(GIF_LOCATION))
                return GIF_LOCATION


def get_queue():
    req = urllib.request.Request("http://{}/queue".format(server_address))
    number_req = json.loads(urllib.request.urlopen(req).read())
    que = len(number_req['queue_pending']) + len(number_req['queue_running'])
    return que



if __name__ == "__main__":
    # 设置工作目录和项目相关的路径
    # WORKING_DIR = 'output'
    # SageMaker_ComfyUI = WORKING_DIR
    workflowfile = 'workflow_api.json.bak'
    COMFYUI_ENDPOINT = '127.0.0.1:8188'
    server_address = COMFYUI_ENDPOINT
    client_id = str(uuid.uuid4())
    seed = random.getrandbits(50)
    prompt = 'Leopards hunt on the grassland'
    print(get_queue())
    generate_clip(prompt, seed, workflowfile, 1)
