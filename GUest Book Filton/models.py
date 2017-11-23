from google.appengine.ext import ndb

class Message(ndb.Model):
    text = ndb.StringProperty()
    name = ndb.StringProperty()
    meil = ndb.StringProperty()
    date=ndb.DateTimeProperty(auto_now_add = True)
