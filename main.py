from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2, urllib, logging
                
from django.utils import simplejson as json

class Beanstalk(webapp.RequestHandler):
    """Handle notifications from Beanstalk"""
    def post(self):
        people=[ "fe9f5e80caa3bf9892f19cc823fff38e" ]
        notifyUrl="http://api.notify.io/v1/notify/"
        apiUrl="?api_key=25e146-7ac02c-f580bf-1a229f"

        str = self.request.get("commit")
        try:
            obj = json.loads( str )
        except ValueError:
            logging.error( "Could not decode JSON" )
            return

        for p in people:
            person_url=notifyUrl+p+apiUrl
            data=urllib.urlencode(
                    [("title", obj['author_full_name']+" committed revision "+
                               unicode(obj['revision']) ),
                     ("text",  '\"'+obj['message']+'\"'),
                     ("icon",  "http://i.imgur.com/VsJyM.png"),
                     ("link",  obj["changeset_url"]),
                     ("sticky", "true")
                    ])
            logging.info( "Sent a notification about Beanstalk revision " + unicode(obj['revision']) )

            try:
                urllib2.urlopen( person_url, data )
            except urllib2.URLError, e:
                logging.error( "Couldn't reach "+person_url )
        
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello thear')

def main():
    """Get the party started on the Saturday night"""
    application = webapp.WSGIApplication(
        [('/', MainPage),
         ('/eatbeans', Beanstalk)],
         debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
