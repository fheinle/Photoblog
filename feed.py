#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" create the rss feed """

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
    """our newsfeed"""
    def get(self):
        """no arguments"""
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
