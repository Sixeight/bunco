# coding: utf-8
from google.appengine.ext import db
from google.appengine.api import users
from model.book import Book

STATUS = {'available': u'在庫あり',
          'occupied': u'貸し出し中',
          'unknown': u'不明'}

class Stock(db.Model):
    book = db.ReferenceProperty(Book,
        required=True, collection_name='stocks')
    owner = db.UserProperty(auto_current_user_add=True)
    status = db.StringProperty(required=True, choices=set(STATUS.keys()), default='available')
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

    def __unicode__(self):
        return STATUS[self.status]

