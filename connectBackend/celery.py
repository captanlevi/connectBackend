import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connectBackend.settings')

app = Celery('connectBackend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



app.conf.beat_schedule = {
    #Scheduler Name
    'move_to_lazy': {
        # Task Name (Name Specified in Decorator)
        'task': 'move_to_lazy',  
        # Schedule      
        'schedule': 10.0,
    },
}  