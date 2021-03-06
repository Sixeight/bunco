
from google.appengine.ext import db

class Comment(db.Model):
    from model.book import Book
    author = db.UserProperty(auto_current_user_add=True)
    body = db.TextProperty(required=True)
    book = db.ReferenceProperty(Book,
        required=True, collection_name='comments')
    created_at = db.DateTimeProperty(auto_now_add=True)

    def path(self):
        return "/comment/" + str(self.key())

    def is_owner(self):
        return self.author in [stock.owner for stock in self.book.stocks]

