#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" helper that displays all public album ids for a user"""

import gdata.photos.service
import sys

gd_client = gdata.photos.service.PhotosService()
gd_client.source = 'photoblog helper script'
try:
    user_name = raw_input('Your picasaweb username: ')
except EOFError:
    sys.exit()
album_list = gd_client.GetUserFeed(user=user_name)
for album in album_list.entry:
    print 'Title: %s ID: %s' % (album.title.text, album.gphoto_id.text)
