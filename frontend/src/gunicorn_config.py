# gunicorn_config.py
bind = "0.0.0.0:10000"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "info"