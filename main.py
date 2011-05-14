from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import urllib2, urllib, logging
                
from django.utils import simplejson as json

class Beanstalk(webapp.RequestHandler):
    ## CONFIG SECTION
    API_KEY="YOUR_API_KEY"
    PEOPLE=[ "MD5_OF_PERSON_EMAIL1", "MD5_OF_PERSON_EMAIL2" ]
    ####

    NOTIFY_URL="http://api.notify.io/v1/notify/"

    def get(self):
        self.error(404)

    """Handle web hook knocking from Beanstalk"""
    def post(self):
        api_url="?api_key="+self.API_KEY

        str = self.request.get("commit")
        try:
            obj = json.loads( str )
        except ValueError:
            logging.error( "Could not decode JSON" )
            return

        for p in self.PEOPLE:
            person_url=self.NOTIFY_URL + p + api_url
            # build a POST data string for notify.io
            data=urllib.urlencode(
                    [("title", obj['author_full_name']+" committed r"+
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
                logging.error( "Couldn't reach notify.io: "+person_url )
        
class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Nothing to see here.')

def main():
    """Get the party started on the Saturday night"""
    application = webapp.WSGIApplication(
        [('/', MainPage),
         ('/eatbeans', Beanstalk)],
         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
