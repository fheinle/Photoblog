#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' send newsletters '''

# Copyright (C) 2009 Florian Heinle
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
