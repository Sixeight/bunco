# coding: utf-8
from google.appengine.ext import db
from google.appengine.api import users
from model.book import Book

STATUS = {0: u'在庫あり',
          1: u'貸し出し中',
          2: u'不明'}

class BookStatus(db.Model):
    book = db.ReferenceProperty(Book,
        required=True, collection_name='statuses')
    owner = db.UserProperty(auto_current_user_add=True)
    modified_add = db.DateTimeProperty(auto_now_add=True,auto_now=True)
    user = users.User()
    status = db.IntegerProperty(required=True, choices=set(STATUS.keys()))

    def __unicode__(self):
        return STATUS[self.status]
