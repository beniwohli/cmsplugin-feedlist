import datetime as dt
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
import feedparser

from cmsplugin_feedlist.models import FeedPlugin
from cmsplugin_feedlist.forms import FeedPluginForm

class FeedCMSPlugin(CMSPluginBase):
    model = FeedPlugin
    name = _('feed plugin')
    form = FeedPluginForm
    CACHE_KEY = 'cmsplugin_feed-cache-%d'
    
    fieldsets = ((None, {'fields': (('title', 'use_feed_title'), 'feed_url', 'template_name', 'items', 'refresh')}),)
    
    def render(self, context, instance, placeholder):
        self.render_template = instance.template_name
        key = self.CACHE_KEY % instance.pk
        feed = cache.get(key, None)
        if not feed:
            feed = feedparser.parse(instance.feed_url)
            if not ('atom' in feed.version or 'rss' in feed.version):
                return context
            if 'bozo_exception' in feed:
                del feed['bozo_exception']
            feed.entries = feed.entries[:instance.items]
            for entry in feed.entries:
                if hasattr(entry, 'updated_parsed'):
                    entry.pubdate = dt.datetime(*entry.updated_parsed[:6])
                elif hasattr(entry, 'date_parsed'):
                    entry.pubdate = dt.datetime(*entry.date_parsed[:6])
                else:
                    entry.pubdate = None
            cache.set(key, feed, timeout=instance.refresh)
        context.update({
            'title': instance.title,
            'entries': feed.entries[:instance.items],
        })
        return context
    
plugin_pool.register_plugin(FeedCMSPlugin)
    
