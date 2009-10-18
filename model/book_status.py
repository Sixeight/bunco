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
    user = users.User()
    modified_add = db.DateTimeProperty(auto_now_add=True,auto_now=True)
    status = db.IntegerProperty()       # STATUS, 0~2

    def __unicode__(self):
        return STATUS[self.status]
