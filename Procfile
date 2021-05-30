web: gunicorn config.wsgi
beat: celery beat -A config -l INFO
worker: celery --app=config worker -l INFO -E
