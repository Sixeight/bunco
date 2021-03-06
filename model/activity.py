# -*- coding: utf-8 -*-
from datetime import date
from google.appengine.ext import db
from google.appengine.api import users
from model.book import Book

import logging

TYPE = {'add':     u'を登録しました',
        'delete':  u'を削除しました',
        'lent':    u'を借りました',
        'back':    u'を返しました',
        'comment': u'にコメントしました'}

class Activity(db.Model):
    type = db.StringProperty(required=True, choices=set(TYPE.keys()))
    book = db.ReferenceProperty(Book, required=True)
    user = db.UserProperty(auto_current_user_add=True)
    created_at = db.DateTimeProperty(auto_now_add = True)

    def action(self):
        return TYPE[self.type]

    def path(self):
        return "/activity/" +  str(self.key())
