#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Update handler, gets new pictures from picasa 

only admins should be allowed to access this."""

import datetime
import logging

import conf
from model import Picture
from utils import EXIF_FMTS, render

from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
import gdata.photos.service
from gdata.alt.appengine import run_on_appengine
run_on_appengine(gdata.photos.service.PhotosService())

class Update(webapp.RequestHandler):
    '''update the datastore with pictures from picasa when called'''
    def __init__(self, *args, **kwargs):
        '''login to google picasa api services'''
        self.gd_client = gdata.photos.service.PhotosService()
        self.gd_client.email = conf.picasaweb_username
        self.gd_client.password = conf.picasaweb_password
        self.gd_client.source = 'photoblog of %s' % conf.picasaweb_username
        self.gd_client.ProgrammaticLogin()
        super(Update, self).__init__(*args, **kwargs)

    def get(self):
        """no arguments"""
        photos = self.gd_client.GetFeed(
            '/data/feed/api/user/%s/albumid/%s?kind=photo' %
            (conf.picasaweb_username, conf.picasaweb_album_id)
        )
        updated_pics, old_pics = [], []
        for photo in photos.entry:
            new_pic = Picture()
            new_pic.public = True
            new_pic.gphoto_id = int(photo.gphoto_id.text)
            new_pic.width = int(photo.width.text)
            new_pic.height = int(photo.height.text)
            new_pic.title = str(photo.title.text)
            # size 64 is cropped to square, which we need for the mosaic
            thumbnail = photo.media.thumbnail[0].url.replace('/s72/', '/s64-c/')
            new_pic.thumbnail = str(thumbnail)
            new_pic.content = str(photo.media.content[0].url)
            new_pic.uploaded = datetime.datetime.strptime(
                    photo.published.text[:-5],
                    '%Y-%m-%dT%H:%M:%S'
            )
            try:
                new_pic.taken = photo.exif.time.datetime()
            except AttributeError: # exif time missing
                new_pic.taken = new_pic.uploaded

            # gdata api provides values as strings. Missing attributes
            # are not empty strings but None, hence need to be taken care of
            for attr in EXIF_FMTS.keys():
                try:
                    exif_value = getattr(photo.exif, attr).text
                    conv_func = EXIF_FMTS[attr]
                    setattr(new_pic,
                            attr,
                            conv_func(exif_value)
                            )
                except (AttributeError, ValueError):
                    # set an empty value for missing keys
                    setattr(new_pic, attr, EXIF_FMTS[attr]())

            try:
                new_pic.flash = bool(photo.exif.flash.text.replace('false',''))
            except AttributeError:
                new_pic.flash = False
            try:
                new_pic.put()
            except db.BadValueError, e:
                if e.args[0].startswith('Picture already stored'):
                    old_pics.append(new_pic)
                    logging.info(e.args[0])
                else:
                    raise
            else:
                updated_pics.append(new_pic)
                logging.info('New picture: %s' % new_pic.gphoto_id)
        logging.debug('Memcache entry for mosaic deleted')
        memcache.delete('mosaic')
        self.response.out.write(
            render('updated.html', {'updated':updated_pics,
                                    'old':old_pics
            }))

application = webapp.WSGIApplication(
        [('/update', Update)],
        debug=True
)

if __name__ == '__main__':
    run_wsgi_app(application)
