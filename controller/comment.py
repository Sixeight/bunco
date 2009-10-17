from google.appengine.api import users
from google.appengine.ext import webapp, db
from model.book import Book
from model.comment import Comment
# from google.appengine.api import memcache
import os
from google.appengine.ext.webapp import template
import logging
import datetime
 
class CommentPage(webapp.RequestHandler):
    def get(self, key):

        # result = memcache.get("index")
        result = False
        if result:
            self.response.out.write(result)
            return

        logging.info("cache not hit()")
        book = Book.get_by_key_name("Book_" + key)
        if book:
            template_values = {
                'book': book,
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/index.html')
            result = template.render(path, template_values)
        else:
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/not_found.html')
            result = template.render(path, template_values)
        # memcache.set("index", result, 600)
        self.response.out.write(result)


    def post(self):
        book = Book.get_by_key_name("Book_" + self.request.get('book'))
        if not book: return
        
        comment = Comment(
            book = book,
            body = self.request.get('body'),
            )
        comment.put()
        self.redirect(book.path())
    
    def put(self, id):
        return
    def delete(self, key):
        comment = Comment.get(db.Key(key))
        if comment:
            comment.delete()
        self.response.out.write("ok")
        return
