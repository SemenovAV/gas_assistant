web: gunicorn --workers=3 config.wsgi
worker: celery --app=config worker -l INFO
