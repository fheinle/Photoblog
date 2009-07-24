#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' create the rss feed '''

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

import datetime

from utils import render
import conf
import PyRSS2Gen
from model import Picture

from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

class Feed(webapp.RequestHandler):
    '''our newsfeed'''
    def get(self):
        '''no arguments'''
        rss = memcache.get('feed')
        
        if rss is None:
            pics = Picture.all()
            t = get_template('feed.xml')
            host = self.request.host_url
            rss = render('feed.xml', {'pics':pics, 'conf':conf,
                                      'host':host})
            memcache.set('feed', rss, time=900)
        self.response.out.write(rss)

application = webapp.WSGIApplication(
        [('/feed', Feed)],
        debug=True
)

if __name__ == '__main__':
    run_wsgi_app(application)
