import os

from twython import Twython

from django.db import models
from django.http import JsonResponse

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

class Story(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    tweet1 = models.URLField(blank=True)
    tweet1_photo = models.URLField(null=True, blank=True)
    tweet1_text = models.TextField(blank=True)
    tweet2 = models.URLField(blank=True)
    tweet2_photo = models.URLField(null=True, blank=True)
    tweet2_text = models.TextField(blank=True)
    tweet3 = models.URLField(blank=True)
    tweet3_photo = models.URLField(null=True, blank=True)
    tweet3_text = models.TextField(blank=True)
    tweet4 = models.URLField(blank=True)
    tweet4_photo = models.URLField(null=True, blank=True)
    tweet4_text = models.TextField(blank=True)
    tweet5 = models.URLField(blank=True)
    tweet5_photo = models.URLField(null=True, blank=True)
    tweet5_text = models.TextField(blank=True)
    
    class Meta:
        app_label = 'fivestory'
        ordering = ('-created',)
        verbose_name_plural = 'Stories'
    
    def __unicode__(self):
        return '{0}'.format(self.name)

    def tweet_url_list(self):
        return filter(None, [self.tweet1, self.tweet2, self.tweet3, self.tweet4, self.tweet5])

    def tweet_ids(self):
        return [str(tweet).split('/')[-1] for tweet in self.tweet_url_list()]
        
    def save(self, *args, **kwargs):
        self.update_twitter_data()
        super(Story, self).save(*args, **kwargs)

    def update_twitter_data(self):
        twitter = Twython(
            TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
        )

        # get the data from Twitter API
        twitter_data = twitter.lookup_status(id=','.join(self.tweet_ids()))

        # so ugly
        for tweet_data in twitter_data:
            tweet_data_id = str(tweet_data['id'])
            tweet_data_media = tweet_data.get('entities').get('media')
            tweet_data_photo = tweet_data_media[0].get('media_url_https') if len(tweet_data_media) else None
            tweet_data_text = tweet_data.get('text')
            if self.tweet1.endswith(tweet_data_id):
                if not self.tweet1_photo: self.tweet1_photo = tweet_data_photo
                if not self.tweet1_text: self.tweet1_text = tweet_data_text
            if self.tweet2.endswith(tweet_data_id):
                if not self.tweet2_photo: self.tweet2_photo = tweet_data_photo
                if not self.tweet2_text: self.tweet2_text = tweet_data_text
            if self.tweet3.endswith(tweet_data_id):
                if not self.tweet3_photo: self.tweet3_photo = tweet_data_photo
                if not self.tweet3_text: self.tweet3_text = tweet_data_text
            if self.tweet4.endswith(tweet_data_id):
                if not self.tweet4_photo: self.tweet4_photo = tweet_data_photo
                if not self.tweet4_text: self.tweet4_text = tweet_data_text
            if self.tweet5.endswith(tweet_data_id):
                if not self.tweet5_photo: self.tweet5_photo = tweet_data_photo
                if not self.tweet5_text: self.tweet5_text = tweet_data_text
        
    