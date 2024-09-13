import json
import websocket
import urllib.request
import urllib.parse
from ai_app import settings

# 加载Comfy配置信息
Comfy_set = settings.COMFYUI_V1
server_address = Comfy_set['server_address']
workflow_dir = Comfy_set['workflow_dir']


# 向服务器队列发送提示词
def queue_prompt(textPrompt, comfy_id):
    p = {"prompt": textPrompt, "client_id": comfy_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


# 获取生成图片
def get_image(fileName, subFolder, folder_type):
    data = {"filename": fileName, "subfolder": subFolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    print("http://{}/view?{}".format(server_address, url_values))
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()


# 获取历史记录
def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


# 获取图片，监听WebSocket消息
def get_images(ws, prompt, comfy_id):
    prompt_id = queue_prompt(prompt, comfy_id)['prompt_id']
    # print('prompt: {}'.format(prompt))
    # print('prompt_id:{}'.format(prompt_id))
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
    # print(history)
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
def parse_worflow(ws, prompt, json_info, comfy_id):
    from .work_api import set_json  #导入对应的json配置函数
    prompt_data = set_json(json_info, prompt)
    return get_images(ws, prompt_data, comfy_id)


# 生成图像并显示
def generate_clip(prompt, idx, workflow_json, comfy_id):
    workflow_file_json = workflow_dir + workflow_json
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, comfy_id))
        print(workflow_file_json)
        images = parse_worflow(ws, prompt, workflow_file_json, comfy_id)
        ws.close()
    except:
        ws.close()
        return 'erro: 监听图片写入失败'
    for node_id in images:
        for image_data in images[node_id]:
            from datetime import datetime
            # 获取当前时间，并格式化为 YYYYMMDDHHMMSS 的格式
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # 使用格式化的时间戳在文件名中
            GIF_LOCATION = "{}/{}_{}.png".format(workflow_dir, idx, timestamp)
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
    # workflowfile = 'workflow_api.json.bak'
    # server_address = '127.0.0.1:8188'
    # client_id = str(uuid.uuid4())
    # prompt = 'Leopards hunt on the grassland'
    # print(get_queue())
    generate_clip('水杯', 1, 'workflow_api.json.bak', '11111111111111111111111111')
