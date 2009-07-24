#!/usr/bin/env python
# -*- coding:utf-8 -*-

''' helper functions '''

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

import os

import conf
from model import Picture
from google.appengine.ext.webapp import template

# mapping of exif attributes to data types in data store
EXIF_FMTS = {
    'exposure':float,
    'fstop':float,
    'make':str,
    'model':str,
    'title':str,
    'iso':int
}

def get_template(name):
    '''get templates from directory structure

    @param name: the filename, sans path
    '''
    templ= os.path.join(
        os.path.dirname(__file__),
        'templates',
        name
    )
    return templ

def render(template_name, context={}):
    '''render the given template with the given content

    includes configuration file contents as conf in templates
    
    @param template_name: template filename, sans path, with extension
    @param context: a dictionary with context information to be included
    '''
    templ = get_template(template_name)
    context.update({'conf':conf})
    return template.render(templ, context)

def _get_newer_or_older(pic, newer=True):
    '''query the database for adjacent pictures
    
    @param pic: center picture
    @param newer: True for LHS, False for RHS
    '''
    if newer:
        options = ('>', 'ASC')
    else:
        options = ('<', 'DESC')
    query = 'WHERE uploaded %s :1 ORDER BY uploaded %s LIMIT 1' % options
    picture = Picture.gql(query, pic.uploaded)
    return picture.get()

def get_newer(pic):
    '''get the next picture'''
    return _get_newer_or_older(pic, newer=True)

def get_older(pic):
    '''get the previous picture'''
    return _get_newer_or_older(pic, newer=False)
