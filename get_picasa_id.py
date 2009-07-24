#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' helper that displays all public album ids for a user'''

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
