#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''Database models'''

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
