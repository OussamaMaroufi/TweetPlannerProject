from __future__ import absolute_import,unicode_literals
import os 
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE','proj.settings')

app = Celery('proj')


app.config_from_object('django.conf:settings',namespace='CELERY')

app.conf.beat_schedule = {
    'every-15-seconds':{
        'task':'api.tasks.send_email',
        'schedule':15,
        # 'args':('oussama@gmail.com',)
        'args':()
    }
}

app.autodiscover_tasks()

#tasks are placed in tasks.py file autodiscover theese tasks for celery to run
