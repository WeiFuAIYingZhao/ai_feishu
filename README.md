启动django   python manage runserver 0.0.0.0:8080

启动celery

-----windwos启动方式  celery -A ai_feishu worker --loglevel=info -P eventlet
  
-----linux启动方式    celery -A ai_feishu worker --loglevel=info

项目依赖包：


pip install Django

pip install celery

pip install websocket websocket-client websockets
