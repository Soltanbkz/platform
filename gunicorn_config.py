command = '/root/code/platform/env/bin/gunicorn'
pythonpath = '/root/code/platform'
bind = '127.0.0.1:8001'
workers = 5
user = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=config.settings'