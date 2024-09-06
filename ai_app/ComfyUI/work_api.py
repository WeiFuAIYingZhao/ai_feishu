import json
import random


def set_json(workflow_json, prompt):
    with open(workflow_json, 'r', encoding="utf-8") as workflow_api_txt2gif_file:
        prompt_data = json.load(workflow_api_txt2gif_file)
        # 设置文本提示
        pre_prompt = "You are a highly imaginative AI art assistant, skilled in describing various scenes to be used as prompts for stable diffusion. I will provide you  a description, and I'd like you to pay special attention to the style of the image I describe. You need to describe the image according to the style I provide, keeping the main content of the scene as close to my description as possible. For secondary elements like backgrounds, you can use your imagination to enrich the overall scene. It's crucial to use very detailed language, building upon the original meaning with intricate artistic techniques to describe the image. Focus on expressing emotions, rendering artistic atmosphere, describing artistic scenes, constructing artistic details, creating artistic themes, describing colors and using professional color applications, choosing perspectives worthy of high-end commercial shots, varying viewpoints freely, and incorporating composition changes inspired by fashion magazine covers. The text must be written in complete paragraphs without titles, section breaks, or numbering. Finally, please output the prompt in professional English:" + prompt
        prompt_data["251"]["inputs"]["text"] = pre_prompt
        # 设置随机数
        prompt_data["236"]["inputs"]["noise_seed"] = random.randint(0, 1000000000000000)
        prompt_data["250"]["inputs"]["seed"] = random.randint(0, 2147483647)
    return prompt_data

if __name__ == '__main__':
    print(set_json('work_api.json','1111111111111111111', '222222222222222222222'))