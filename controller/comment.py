from google.appengine.api import users
from google.appengine.ext import webapp, db
from model.book import Book
from model.comment import Comment
from model.activity import Activity
# from google.appengine.api import memcache
import os
from google.appengine.ext.webapp import template
import logging
import datetime
 
class CommentPage(webapp.RequestHandler):
    def get(self, key):
        try:
            comment = Comment.get(db.Key(key))
        except(Exception):
            comment = None
        if comment:
            template_values = {
                'comment': comment,
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'comment/index.html')
            result = template.render(path, template_values)
        else:
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'comment/not_found.html')
            result = template.render(path, {})
        self.response.out.write(result)

    def post(self):
        book = Book.get_by_key_name("Book_" + self.request.get('book'))
        if not book: return
        body = self.request.get('body')
        if not body: return
        comment = Comment(
            book = book,
            body = body
            )
        comment.put()
        Activity(type='comment', book=book).put()
        user = users.get_current_user()
        template_values = {
            'comment': comment,
            'user': user,
            }
        path = os.path.join(os.path.dirname(__file__), '..', 'view', 'comment/index.html')
        result = template.render(path, template_values)
        self.response.out.write(result)

    def put(self, id):
        return

    def delete(self, key):
        comment = Comment.get(db.Key(key))
        user = users.get_current_user()
        if comment and user and user == comment.author:
            comment.delete()
            self.response.out.write("ok")
