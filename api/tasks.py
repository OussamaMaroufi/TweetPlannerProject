#here to build some tasks for celery to run 
from __future__ import absolute_import,unicode_literals


from celery import shared_task
import time

#implement fetch posts from database with the current date and and push it over tweeter api 

from .models import Post


@shared_task
def send_email():
    # print(Post.objects.all())
    print(f'A sample message is sent to')
    