web: gunicorn config.wsgi
beat: celery --app=config beat -l INFO
worker: celery --app=config worker -l INFO -E
