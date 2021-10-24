celery -A connectBackend beat -l info --logfile=celery.beat.log --detach
celery -A connectBackend worker -l info --logfile=celery.log --detach
python3 manage.py runserver 0.0.0.0:8000