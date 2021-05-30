web: gunicorn config.wsgi
worker: celery --app=config worker -l INFO -E
