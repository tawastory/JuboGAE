from google.appengine.ext import db  # @UnresolvedImport

class Jubo_Am(db.Model):
    firsthymn = db.IntegerProperty()
    psalm = db.StringProperty()
    secondhymn = db.IntegerProperty()
    scripture = db.StringProperty()
    sermon = db.StringProperty()
    offertory = db.IntegerProperty()
    
class User(db.Model):
    id = db.StringProperty()
    password = db.StringProperty()