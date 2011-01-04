#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='cmsplugin_feedlist',
    version='0.0.1',
    author='Benjamin Wohlwend',
    author_email='bw@piquadrat.ch',
    url='http://github.com/piquadrat',
    description = 'django CMS feedlist plugin to display a list of items from '\
                  'an RSS/Atom feed',
    packages=find_packages(),
    package_data={
        'cmsplugin_feedlist': [
            'templates/cmsplugin_feedlist/base.html',
            'templates/cmsplugin_feedlist/feed_templates/*.html',            
        ],
    },
    provides=['cmsplugin_feedlist',],
    include_package_data=True,
    license='BSD License',
)