import database as db
from flask import request, session
from datetime import datetime

def create_message_feed():
    posts = {}
    posts.setdefault("username",session["user"]["username"])
    posts.setdefault("messagedate",datetime.utcnow())
    posts_details = []
    feed = request.form.get('message')
    posts_details.append({"message":feed})

    posts.setdefault("messages",posts_details)
    db.create_posts(posts)
