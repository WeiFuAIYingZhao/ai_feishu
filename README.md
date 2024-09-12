+ 项目全局参数更改
1.   ai_feishu/ai_feishu/settings.py文件更改
```
    CELERY_BROKER_URL=‘服务器数据库文件所在位置’
    CELERY_RESULT_BACKEND=‘服务器数据库文件所在位置’
```
2.  ai_feishu/ai_app/settings.py文件修改
```angular2html
    FEISHU_V2_SDK_CONFIGS对应的参数修改
    COMFYUI_V1对应的参数修改
```
+ ComfyUI的工作流添加设计文件说明
1. ai_feishu/ComfyUI 目录下
```angular2html
工作流json文件 work_api.json
创建同名的参数修改文件  work_api.py 按照现有修改即可
加载工作流配置  Comfy_api.py里parse_worflow这个方法里进行相应导入，只修改from .对应的修改参数文件名。
from .work_api import set_json  #导入对应的json配置函数
```

+ 启动django  
`python manage runserver 0.0.0.0:8080`
+ 启动celery
```
   windwos启动方式:  
     celery -A ai_feishu worker --loglevel=info -P eventlet  
   linux启动方式:  
     celery -A ai_feishu worker --loglevel=info
```
+ 项目依赖包:  
```angular2html
    pip install Django  
    pip install celery  
    pip install websocket websocket-client
    pip install requests requests_toolbelt
    pip install pydantic
    pip install sqlalchemy
    pip install cryptography
    pip install pycryptodome
    # eventlet插件 Windows安装，linux无需安装
    pip install eventlet
```
+ 项目结构  
```angular2html
 |-- ai_app # app代码实现部分
    |-- settings.py # 飞书，ComfyUI配置部分
 |-- ai_feishu # django项目框架部分
 |-- db.sqlite3 # 异步队列使用库文件--会自动创建
 |-- manage.py #  启动文件
 |-- README.md
```
