
from google.appengine.ext import webapp
from model.book import Book
from model.stock import Stock
# from google.appengine.api import memcache
from google.appengine.api import users
import os
from google.appengine.ext.webapp import template
import logging
import datetime
from model.book import CantBuildBook
import re

class BookPage(webapp.RequestHandler):
    def get(self, key):

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
        # FIXME: need exception
        if not users.get_current_user():
            return
        # FIXME: very dirty
        isbn = self.request.get('isbn')
        r = re.compile('http://[^\d]+/(([X\d])+)/?.*')
        if r.match(isbn):
            isbn = r.match(isbn).group(1)
        book = Book(
            key_name = "Book_" + isbn,
            isbn = isbn
            )
        try:
            book.build_from_isbn()
        except CantBuildBook:
            self.redirect('/')
            return
        book.put()
        Stock(book=book).put()
        self.redirect(book.path())

    def put(self, key):
        if not users.get_current_user():
            self.response.out.write("deny")
            return
        book = Book.get_by_key_name("Book_" + key)
        if not book:
            self.response.out.write("ng")
            return
        book.lent_or_return()
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
        self.response.out.write("ok")
        return

