
from google.appengine.ext import webapp
from model.book import Book
from model.stock import Stock
from model.activity import Activity
# from google.appengine.api import memcache
from google.appengine.api import users
import os
from google.appengine.ext.webapp import template
import logging
import datetime
from model.book import CantBuildBook

class BookPage(webapp.RequestHandler):
    def get(self, key):
        if key == 'add':
            self.post()
            return
        # result = memcache.get("index")
        result = False
        if result:
            self.response.out.write(result)
            return

        user = users.get_current_user()
        if user:
            greeting = ("<a href=\"%s\">logout %s</a>" %
                        (users.create_logout_url("/"), user.nickname()))
        else:
            greeting = ("<a href=\"%s\">login</a>" %
                        users.create_login_url("/"))

        logging.info("cache not hit()")
        book = Book.get_by_key_name("Book_" + key)
        template_values = None
        if book:
            template_values = {
                'user': user,
                'book': book,
                'greeting': greeting,
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/index.html')
            result = template.render(path, template_values)
        else:
            template_values = {
                'user': user,
                'key':  key,
                'greeting': greeting,
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'book/not_found.html')
            result = template.render(path, template_values)
        # memcache.set("index", result, 600)
        self.response.out.write(result)


    def post(self):
        # FIXME: need exception
        if not users.get_current_user():
            return
        book = Book.create_from_isbn(self.request.get('isbn'))
        if not book.title:
            try:
                book.build_from_isbn()
            except CantBuildBook:
                self.redirect('/')
                return
            book.put()
        
        if self.request.get('owner'):
            owner = users.User(email = self.request.get('owner'))
        else:
            owner = users.get_current_user()
        Stock(book=book, owner=owner).put()
        Activity(type='add', book=book).put()
        self.redirect(book.path())

    def put(self, key):
        if not users.get_current_user():
            self.response.out.write("deny")
            return
        book = Book.get_by_key_name("Book_" + key)
        if not book:
            self.response.out.write("ng")
            return
        if self.request.get('description'):
            stock = book.mystock()
            if stock:
                stock.description = self.request.get('description')
                stock.put()
                self.response.out.write(self.request.get('ok'))
                return
            else:
                self.response.out.write('no stock');
                return
        else:
            type = book.lent_or_return()
            Activity(type=type, book=book).put()
        return


    def delete(self, key):
        # FIXME: dirty
        if not users.is_current_user_admin():
            return
        book = Book.get_by_key_name("Book_" + key)
        if book:
            for comment in book.comments: comment.delete()
            for stock in book.stocks: stock.delete()
            book.delete()
        Activity(type='delete', book=book).put()
        self.response.out.write("ok")
        return

