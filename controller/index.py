
from google.appengine.ext import webapp
from model.book import Book
# from google.appengine.api import memcache
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
import logging

class IndexPage(webapp.RequestHandler):
    def get(self):
        # result = memcache.get("index")
        result = False
        if not result:
            logging.info("cache not hit(index)")
            user = users.get_current_user()
            if user:
                greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                            (user.nickname(), users.create_logout_url("/")))
            else:
                greeting = ("<a href=\"%s\">Sign in or register</a>." %
                            users.create_login_url("/"))

            template_values = {
                'greeting': greeting,
                'user': user,
                'books': Book.all().order('-created_at').fetch(1000),
                }
            path = os.path.join(os.path.dirname(__file__), '..', 'view', 'index.html')
            result = template.render(path, template_values)
            # memcache.set("index", result, 600)

        self.response.out.write(result)

