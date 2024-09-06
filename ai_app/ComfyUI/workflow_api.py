import json


def set_json(workflow_json, prompt, seed):
    with open(workflow_json, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
        prompt_data = json.load(workflow_api_txt2gif_file)
        # 设置文本提示
        prompt_data["6"]["inputs"]["text"] = prompt
        # 设置随机数
        prompt_data["3"]["inputs"]["seed"] = seed
    return prompt_data
