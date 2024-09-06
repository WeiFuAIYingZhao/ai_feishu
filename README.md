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
