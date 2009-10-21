# -*- coding: utf-8 -*-
from datetime import date
from google.appengine.ext import db
from google.appengine.api import users
from model.book import Book

import logging

TYPE = {'add':     u'を提供してくれました',
        'delete':  u'を削除しました',
        'lent':    u'を借りました',
        'back':    u'を返しました',
        'comment': u'にコメントしました'}

class Activity(db.Model):
    type = db.StringProperty(required=True, choices=set(TYPE.keys()))
    book = db.ReferenceProperty(Book, required=True)
    user = db.UserProperty(auto_current_user_add=True)
    created_at = db.DateTimeProperty(auto_now_add = True)

    def __repr__(self):
        if self.user == None:
            nickname = u'Anonymous'
        else:
            nickname = self.user.nickname()
        return nickname             + \
                   u'さんが「'      + \
                   u'<a href="'     + \
                   self.book.path() + \
                   u'">'            + \
                   self.book.title  + \
                   u'</a>」'        + \
                   TYPE[self.type]

