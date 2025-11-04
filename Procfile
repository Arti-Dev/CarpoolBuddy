release: python manage.py migrate
web: gunicorn project.wsgi
# web: daphne -b 0.0.0.0 -p $PORT project.asgi:application