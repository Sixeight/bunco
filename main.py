import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
# from controller.api import WordPage,WordsPage
from controller.index import IndexPage
from controller.book import BookPage
from controller.comment import CommentPage

application = webapp.WSGIApplication(
  [
#    ('/api/words', WordsPage),
#    ('/api/word', WordPage),
    ('/', IndexPage),
    ('/book', BookPage),
    (r'/book/(.*)', BookPage),
    ('/comment', CommentPage),
    (r'/comment/(.*)', CommentPage),
    ],
  debug=True)
 
def main():
  run_wsgi_app(application)
 
if __name__ == "__main__":
  main()
