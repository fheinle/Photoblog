#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' the photoblog '''

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

import logging
from random import random

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.api import memcache

from model import Picture
from utils import render, get_newer, get_older

class List(webapp.RequestHandler):
    '''List all pictures in the datastore'''
    def get(self):
        '''no arguments'''
        page = memcache.get('mosaic')
        if page is None:
            pics = Picture.all()
            page = render('list.html', {'pics':pics})
            if not memcache.add('mosaic', page, 2419200):
                logging.error('Mosaic not written to memcache')
            else:
                logging.debug('New memcache entry: mosaic')
        logging.debug('All pictures listed')
        self.response.out.write(page)

class Random(webapp.RequestHandler):
    '''redirect to a random picture'''
    def get(self):
        '''no arguments'''
        random_pic = Picture.gql(
            'WHERE rand > :1 ORDER BY rand LIMIT 1',
            random()
                ).get()
        logging.debug('Random Picture: %s' % random_pic)
        self.redirect('/photo/%s' % random_pic.gphoto_id)

class Photo(webapp.RequestHandler):
    '''display individual pictures'''
    def get(self, gphoto_id=None):
        '''display the picture
        @param gphoto_id: the numeric ID from picasa
        '''
        if not gphoto_id:
            query = Picture.gql('ORDER BY uploaded DESC LIMIT 1')
            latest_picture = query.get()
            gphoto_id = str(latest_picture.gphoto_id)
        page = memcache.get(gphoto_id, namespace='pics')
        if page is None:
            pics = Picture.all().filter('gphoto_id =', int(gphoto_id))
            pic = pics.get()
            logging.debug('Picture view: %s' % pic.gphoto_id)
            page = render('pic.html', {'pic':pic,
                                        'next':get_newer(pic),
                                        'prev':get_older(pic)
            })
            if not memcache.add(gphoto_id, page, 86400, namespace='pics'):
                logging.error('Page %s not written to memcache' % gphoto_id)
            else:
                logging.debug('New memcache entry: %s' % gphoto_id)
        self.response.out.write(page)

class About(webapp.RequestHandler):
    '''small about page'''
    def get(self):
        '''no arguments'''
        self.response.out.write(render('about.html'))

application = webapp.WSGIApplication(
        [('/', Photo),
         ('/info', About),
         ('/mosaic', List),
         ("/zufall", Random),
         ('/photo/(?P<pic>\d+)', Photo)],
        debug=True
)

if __name__ == '__main__':
    run_wsgi_app(application)
