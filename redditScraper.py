import praw
import datetime
import random
import os
import urllib.request as req
import argparse
import pandas as pd
import requests



user_agent = 'pc:pythonBot:v1 (by /u/No-Desk-5113)'
client_id = 'tsQzGU_eCwFkZw'
client_secret = 'Vutq--oPlXzITc4RQkOI4FkM_RbVrA'

class RedditHandler():
    def __init__(self, reddit):
        self.reddit = reddit
        self.post_urls = []
        self.post_title= [] 
        self.post_description = []
        self.post_title = [] 
        self.post_id = [] 
        self.post_time = [] 
        self.post_score = []
    def get_posts(self, number, subreddit, type):
        sub = self.reddit.subreddit(subreddit)
        allowed_types = ['hot', 'new', 'rising', 'top']
        if type.lower() not in allowed_types:
            raise TypeError('Not a valid type. Please use only hot, new, rising or top')
        else:
            idx = allowed_types.index(type.lower())
            if idx == 0:
                posts = sub.hot(limit = number)
                for post in posts:
                    self.post_urls.append(post.url.encode('utf-8'))
                    self.post_title.append(post.title)
                    self.post_score.append(post.score)
                    self.post_time.append(datetime.datetime.fromtimestamp(post.created))
                    self.post_id.append(post.id)
            elif idx == 1:
                posts = sub.new(limit = number)
                for post in posts:
                    self.post_urls.append(post.url.encode('utf-8'))
                    self.post_title.append(post.title)
                    self.post_score.append(post.score)
                    self.post_time.append(datetime.datetime.fromtimestamp(post.created))
                    self.post_id.append(post.id)
            elif idx == 2:
                posts = sub.rising(limit = number)
                for post in posts:
                    self.post_urls.append(post.url.encode('utf-8'))
                    self.post_title.append(post.title.encode('utf-8'))
                    self.post_score.append(post.score)
                    self.post_time.append(datetime.datetime.fromtimestamp(post.created))
                    self.post_id.append(post.id)
            else:
                x = ["all", "hour", "month", "day", "year", "week"]
                i = random.randint(0, len(x))
                posts = sub.top(x[i], limit=number )
                for post in posts:
                    self.post_urls.append(post.url.encode('utf-8'))
                    self.post_title.append(post.title.encode('utf-8'))
                    self.post_score.append(post.score)
                    self.post_time.append(datetime.datetime.fromtimestamp(post.created))
                    self.post_id.append(post.id)
        return self.post_title

    def save_all(self, subreddit):
        print(">>Writing Everything to Disk. The data of ", subreddit, "is being saved....")

        dirpath = os.path.join('./', subreddit)
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        for ind, url in enumerate(self.post_urls):
            _, ext = os.path.splitext(url)
            try:
                print('dowloading>>>>>>', self.post_urls[ind])
                # k = self.post_urls[ind][1:]
                # print(k)
                print(type(dirpath), type(self.post_title[ind]), type(ext))
                req.urlretrieve(self.post_urls[ind].decode('utf-8'), dirpath+self.post_title[ind]+ext.decode("utf-8"))
            except Exception as e:
                print('Something when wrong :( <<<<<', e)

            
reddit = praw.Reddit(client_id=client_id, client_secret = client_secret,
                        user_agent = user_agent)

handle = RedditHandler(reddit)
a = handle.get_posts(10, 'wholesomememes', 'hot')
handle.save_all('wholesomememes')

# sub = reddit.subreddit('ProgrammerHumor')
# posts = sub.rising(limit=10)

# for post in posts:
#     print(post.title.encode('utf-8'))

