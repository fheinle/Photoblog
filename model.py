#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''Database models'''

from random import random
from google.appengine.ext import db

class Subscription(db.Model):
    email = db.EmailProperty()
    validation_key = db.StringProperty()
    active = db.BooleanProperty()

class Picture(db.Model):
    '''maps to a picture in picasa'''
    public = db.BooleanProperty()
    gphoto_id = db.IntegerProperty()
    height = db.IntegerProperty()
    width = db.IntegerProperty()
    exposure = db.FloatProperty()
    flash = db.BooleanProperty()
    fstop = db.FloatProperty()
    iso = db.IntegerProperty()
    make = db.StringProperty()
    model = db.StringProperty()
    title = db.StringProperty()
    thumbnail = db.LinkProperty()
    content = db.LinkProperty()
    taken = db.DateTimeProperty()
    uploaded = db.DateTimeProperty()
    rand = db.FloatProperty()

    def put(self):
        '''only save new pictures'''
        pics = Picture.all().filter('gphoto_id =', self.gphoto_id)
        if pics.count():
            raise db.BadValueError('Picture already stored: %s' %
                                    self.gphoto_id)
        # assign random number to every picture, makes it easier to 
        # return random pictures later. First one needs to be 1
        all_pics = Picture.all()
        if all_pics.count(): 
            self.rand = random()
        else:
            self.rand = 1.0
        super(Picture, self).put()
