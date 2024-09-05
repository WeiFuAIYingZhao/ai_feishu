import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_feishu.settings')

from celery import Celery, shared_task


# 启动worker的命名
app = Celery('ai_feishu')

# 自动检索前缀为CELERY的配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动搜索每个app中的tasks.py文件
app.autodiscover_tasks()