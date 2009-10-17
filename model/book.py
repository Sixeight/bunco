
from google.appengine.ext import db

class Book(db.Model):
    isbn         = db.StringProperty()
    title        = db.StringProperty()
    author       = db.StringProperty()
    publisher    = db.StringProperty()
    published_at = db.DateProperty()
    created_at   = db.DateTimeProperty(auto_now_add = True)

    def path(self):
        return "/book/" + self.isbn

