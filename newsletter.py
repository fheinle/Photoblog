#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' send newsletters '''

from datetime import datetime
from google.appengine.api import mail
from google.appengine.ext import webapp

from model import Subscription, Picture
from util import render
import conf

class Newsletter(webapp.RequestHandler):
    '''send newsletters to subscribed recipients'''
    def get(self):
        '''no arguments'''
        query = Subscription.all().filter('active =', True)
        recipients = query.fetch()
        today = datetime.today()
        query = Picture.all().filter('uploaded >', 
                datetime(today.year, today.month, today.day, 0, 0)
        )
        pictures_today = query.fetch()
        message = mail.EmailMessage()
        message.to = conf.mail_from_address
        message.bcc = [r.email for r in recipients]
        message.subject = conf.mail_newsletter_subject
        message.body = render('newsletter.txt', {'pics':pictures_today})
        message.send()

application = webapp.WSGIApplication(
        [('/send-newsletter', Newsletter)],
        debug=True
)

if __name__ == '__main__':
    run_wsgi_app(application)
