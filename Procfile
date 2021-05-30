web: gunicorn config.wsgi
beat: celery beat --app=config -l INFO
worker: celery --app=config worker -l INFO -E
