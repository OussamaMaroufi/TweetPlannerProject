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

# Create API object
api = tweepy.API(auth)

# Create a tweet





def job():
    
    before = str(dt.datetime.now()- timedelta(minutes=5))
    next = str(dt.datetime.now()+ timedelta(minutes=5))
    print('befor:aftre',before,next)

    try:

        con = lite.connect('db.sqlite3')

        cur = con.cursor()
        s = f'SELECT * FROM api_post  Where  postTime > "{before}" and postTime < "{next}"'
        print(s)
        cur.execute(f'SELECT * FROM api_post  Where  postTime > "{before}" and postTime < "{next}"')

        datas = cur.fetchall()
        print(datas)
        for data in datas:
            print(data)
            if data[4] == 0:
                if data[6] == "" or len(data[6]) == 0:
                    status = api.update_status(data[1])
                else:
                    status = api.update_status_with_media(status=data[1],filename=rf"/home/oussama/Fronted/feedback/media/{data[6]}")                
                cur.execute(f'update api_post set isPublished=1,postLink="https://twitter.com/i/web/status/{status.id}" where id = {data[0]}')

                con.commit()
                
  

    except Exception as e:
        print ("Error {}:".format(e.args[0]))
        sys.exit(1)

    finally:

        if con:
            con.close()


schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
