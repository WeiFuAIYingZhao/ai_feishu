#  飞书认证配置
FEISHU_V2_SDK_CONFIGS = {
    'FEISHU_APP_ID': "cli_a64782806209500c",  # 企业应用的id
    'FEISHU_APP_SECRET': "XynnovfZD9oduvcRqi12scCLX1mAkMCz",  # 企业应用的SECRET
    'FEISHU_VERIFY_TOKEN': "0OpagCtMBZ3Mawd0RrPEU6vSAyaFXjXw",  # 企业应用的事件加密token
    'FEISHU_ENCRYPT_KEY': "xA34g2v8xRXIfcx7arQ20fHQBGl5xjiU",  # 企业应用的事件加密key
}


# ComfyUI配置
# WORKING_DIR字段设置图片工作目录
# workflow_dir字段设置ComfyUI的工作流json目录
COMFYUI_V1 = {
    'server_address': '127.0.0.1:8188',
    'WORKING_DIR': 'D:/django-env/ai_feishu/ai_app/output',
    'workflow_dir': 'D:/django-env/ai_feishu/ai_app/ComfyUI/'
}