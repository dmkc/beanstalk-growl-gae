# beanstalk-growl-gae
This little script allows you to receive local Growl notifications
about commits on Beanstalk using [notify.io](http://notify.io) and Google App Engine.

## Installation
1. Install [notify.io](http://notify.io).
1. In the settings for Notify.io mark the **Yes, I want to send notifications with this account** checkmark.
1. Check out the source and edit `main.py` to contain your Notify.io 
API key and MD5 hashes of all users that you want notified of Beanstalk commits. 
1. Set up a Google App Engine app. Edit `app.yaml` to set your app's name to whatever you set on App Engine's website. Deploy the app.
1. Configure a [Beanstalk web hook](http://support.beanstalkapp.com/customer/portal/articles/68110-trigger-a-url-on-commit-with-web-hooks) and point to `http://yourapp.appspot.com/eatbeans`.

That should be it! You'll receive a Growl notificaton any time there is Beanstalk commit, with a link to the commit's page and a pretty icon.
