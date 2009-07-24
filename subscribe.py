#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" subscription handling """

from model import Subscription
from utils import render
import conf

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import mail

from uuid import uuid4 as uuid
import logging

class Subscribe(webapp.RequestHandler):
    """Handle subscription and send confirmation mails"""
    def get(self):
        """initial call, render and show the form"""
        error = bool(self.request.GET.get('error', None))
        self.response.out.write(render('subscribe.html', {'error':error}))
    
    def post(self):
        """email address has been entered
        
        validate and send the confirmation mail"""
        to_address_1 = self.request.get('to_1')
        to_address_2 = self.request.get('to_2')
        if not to_address_1 == to_address_2:
            self.redirect('/abo/subscribe?error=mails')
        else:
            key = str(uuid().int)
            logging.error('%s' % key)
            confirmation_link = '%s/abo/confirm/%s' % (conf.host, key)
            mail_content = render('subscribe_mail.txt',
                    {'link':confirmation_link,
                     'host':conf.host,
                     'sender_mail':conf.mail_from_address,
                     'sender_name':conf.mail_from_name
                    }
            )
            query = Subscription.all().filter('email =', to_address_1)
            if query.count(): # email has been submitted before
                prev_mail = query.get()
                if prev_mail.active:
                    logging.debug('Repeat subscription: %s' % prev_mail.email)
                    self.redirect('/abo/success')
                else:
                    logging.debug('New subscription key for %s' %
                            prev_mail.email)
                    prev_mail.delete()
            subscription = Subscription(email=to_address_1,
                               validation_key=key,
                               active=False)
            subscription.put()
            logging.info('New subscription: %s' % subscription.email)
            logging.debug('Sending confirmation mail to %s' % to_address_1)
            mail.send_mail(
                sender="%s (Photoblog) <%s>" % (conf.mail_from_name,
                                                conf.mail_from_address
                                                ),
                to=to_address_1,
                subject="Bestätigung Ihrer Mail-Adresse",
                body = mail_content
            )
            self.redirect('/abo/success')

class Confirm(webapp.RequestHandler):
    """activate email subscription"""
    def get(self, key):
        """check if the given key is valid"""
        query = Subscription.all().filter('validation_key =', key)
        if not query.count():
            logging.debug('Subscription failed with key %s' % key)
            resp = render('abo_subscribe_wrong_key.html')
        else:
            subscription = query.get()
            subscription.active = True
            subscription.put()
            logging.info('New subscription: %s' % subscription.email)
            resp = render('abo_subscribe_complete.html')
        self.response.out.write(resp)

class Unsubscribe(webapp.RequestHandler):
    """unsubscribe an address"""
    def get(self, address):
        address = unquote_plus(address)
        query = Subscription.all().filter('email =', address)
        if not query.count() == 1:
            logging.debug('Failed unsubscription: %s' % address)
            resp = render('abo_unsubscribe_failed.html')
        else:
            subscription = query.get()
            subscription.active = False
            subscription.put()
            logging.info('Unsubscribed %s' % address)
            resp = render('abo_unsubscribe_successful.html')
        self.response.out.write(resp)

class Status(webapp.RequestHandler):
    """display success info"""
    def get(self):
        """doesn't do much"""
        mails = Subscription.all()
        self.response.out.write(render('abo_subscribe.html', {'mails':mails}))

application = webapp.WSGIApplication(
        [('/abo/subscribe', Subscribe),
        ('/abo/confirm/(?P<key>\d+)/?', Confirm),
        ('/abo/success', Status)],
        debug=True
)

if __name__ == '__main__':
    run_wsgi_app(application)
