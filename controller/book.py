
from google.appengine.ext import webapp
from model.book import Book
# from google.appengine.api import memcache
from google.appengine.api import users
import os
from google.appengine.ext.webapp import template
import logging
import datetime
 
class BookPage(webapp.RequestHandler):
    def get(self, key):

        # result = memcache.get("index")
        result = False
        if result:
            self.response.out.write(result)
            return

        user = users.get_current_user()
        if user:
            greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                        (user.nickname(), users.create_logout_url("/")))
        else:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/"))
        
        logging.info("cache not hit()")
        book = Book.get_by_key_name("Book_" + key)
        if book:
            template_values = {
                'user': user,
                'book': book,
                'greeting': greeting,
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/index.html')
            result = template.render(path, template_values)
        else:
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/not_found.html')
            result = template.render(path, template_values)
        # memcache.set("index", result, 600)
        self.response.out.write(result)


    def post(self):
        book = Book(
            key_name = "Book_" + self.request.get('isbn'),
            isbn = self.request.get('isbn'),
            title = self.request.get('title'),
            author = self.request.get('author'),
            publisher = self.request.get('publisher'),
            )
        book.published_at = datetime.date.today() # XXX
        book.put()
        self.redirect(book.path())
    
    def put(self, key):
        return
    def delete(self, key):
        book = Book.get_by_key_name("Book_" + key)
        if book:
            book.delete()
        self.response.out.write("ok")
        return
