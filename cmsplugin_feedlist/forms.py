from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext

import feedparser

from models import FeedPlugin

class FeedPluginForm(forms.ModelForm):
    use_feed_title = forms.BooleanField(label=_('use feed title'), initial=False, required=False)
    
    def clean_feed_url(self):
        self.feed = feedparser.parse(self.cleaned_data['feed_url'])
        if not ('atom' in self.feed.version or 'rss' in self.feed.version):
            raise forms.ValidationError(_("This isn't a valid RSS or Atom feed"))
        return self.cleaned_data['feed_url']
    
    def clean(self):
        cleaned_data = super(FeedPluginForm, self).clean()
        if cleaned_data.get('use_feed_title'):
            if 'title' in self.feed.feed:
                cleaned_data['title'] = self.feed.feed.title
            else:
                self._errors['title'] = self.error_class([ugettext('Feed contains no title')])
        return cleaned_data
            
    class Meta:
        model = FeedPlugin
    