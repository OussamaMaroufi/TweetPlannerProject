import datetime
from posixpath import abspath
from django.db.models.fields import DateTimeField
import schedule
import time
import sqlite3 as lite
import sys
import datetime as dt
from datetime import timedelta
import tweepy

# Authenticate to Twitter
CONSUMER_KEY="MIjW7DBTApxe3OklVxM6wbqSk"
CONSUMER_SECRET="nFSjeJ1aCj6ZXg9l3TWSVK7GHF7peONAKyqrg0s2Vj6IWS4PFQ"
ACCESS_TOKEN="1286552388-LvRblvp2b6l3fS6KzuAb7fPI9nYnpBtRzLTRWeo"
ACCESS_TOKEN_SECRET="mkgqWYMSze2DDAHca47H8szPTa9t5bewyn4GnSu1R3B8P"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
from django.utils import timezone
# Create API object
api = tweepy.API(auth)

# Create a tweet
import django,os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
django.setup()
from api.models import Post




def job():
    
    before = str(timezone.now()-timedelta(minutes=5) ) 
    next = str(timezone.now()+ timedelta(minutes=5))

    abspath=os.path.dirname(os.path.abspath(__file__))
    posts=Post.objects.filter(isPublished=False)
    print(Post.objects.all())
    
    posts=posts.filter(postTime__gt=before).values_list('pk',flat=True)
    print(before,next,posts)
    try:
        pass
        for p in list(posts):
            _post=Post.objects.get(pk=int(p))
            if not _post.postImage:
                status=api.update_status(_post.content)

                _post.isPublished=True
                _post.postLink=rf"https://twitter.com/i/web/status/{status.id}"

                _post.save()
            else:
                status= api.update_status_with_media(status=_post.content,filename=rf"{abspath}/media/{_post.postImage}")

                _post.isPublished=True
                _post.postLink=rf"https://twitter.com/i/web/status/{status.id}"

                _post.save()
           
    except Exception as e:
        print(e)
        pass

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
