import os, glob

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

def get_templates():
    templates = set()
    paths = list(settings.TEMPLATE_DIRS)
    paths.append(os.path.join(os.path.dirname(__file__), 'templates'))
    for path in paths:
        for t in glob.glob(os.path.join(path, 'cmsplugin_feedlist', 'feed_templates', '') + '*.html'):
            t = t.replace(path, '')[1:]
            templates.add(t)
    
    return tuple((t, os.path.split(t)[-1]) for t in sorted(templates))

class FeedPlugin(CMSPlugin):    
    title = models.CharField(_('title'), max_length=100, blank=True, default='')
    feed_url = models.URLField(_('URL'),)
    template_name = models.CharField(_('template'), max_length=100, blank=True, default='', choices=get_templates())
    items = models.PositiveIntegerField(_('items'), default=5)
    refresh = models.PositiveIntegerField(_('refresh time'), default=15*60, help_text=_('in seconds'))
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('feed plugin')
        verbose_name_plural = _('feed plugins')