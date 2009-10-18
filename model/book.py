
from google.appengine.ext import db
from google.appengine.api import urlfetch
import yaml
from datetime import date

class CantBuildBook(Exception):
     def __init__(self, value):
         self.value = value
     def __str__(self):
         return repr(self.value)

class Book(db.Model):
    isbn         = db.StringProperty()
    title        = db.StringProperty()
    author       = db.StringProperty()
    publisher    = db.StringProperty()
    published_at = db.DateProperty()
    created_at   = db.DateTimeProperty(auto_now_add = True)

    def path(self):
        return "/book/" + self.isbn

    def image_path(self, size = 'M'):
        return 'http://images-jp.amazon.com/images/P/' + self.isbn + '.09._SC' + size + 'ZZZZZZ_PA30,0,0,30_SY300_.jpg'

    def large_image_path(self):
        return self.image_path('L')

    def amazon_path(self):
        return 'http://amazon.jp/dp/' + self.isbn

    def build_from_isbn(self):
        url = 'http://api.dan.co.jp/asin/' + self.isbn + '.yml'
        result = urlfetch.fetch(url)

        if result.status_code != 200:
            raise CantBuildBook, 'Maybe, invalid ISBN'

        try:
            info = yaml.load(result.content)['ItemAttributes']

            if info.has_key('Author'):
                self.author = info['Author']
            elif info.has_key('Creator'):
                creators = []
                for person in info['Creator']:
                    creators.append(person['content'] + ' (' + person['Role'] + ')')
                self.author = ', '.join(creators)

            self.title = info['Title']
            pub_date = info['PublicationDate']
            self.publisher = info['Publisher']

            if pub_date.__class__ == str:
                pub_date = map(int, pub_date.split('-'))
                if len(pub_date) < 3:
                    pub_date.append(1)
                self.published_at = date(*pub_date)
                return
            self.published_at = pub_date
        except CantBuildBook, e:
            raise CantBuildBook, e.value
        except Exception:
            raise CantBuildBook, 'Unknown Error'

    def stock_number(self):
         return self.statuses.filter('status = ', 0).count()
