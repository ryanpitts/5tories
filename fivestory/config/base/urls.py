from django.conf import settings
from django.conf.urls import url, patterns, include
from django.contrib import admin

from fivestory.apps.fivestory.views import StoryListView, StoryDetailView, api

urlpatterns = patterns('',
    url(
        regex   = '^$',
        view    = StoryListView.as_view(),
        kwargs  = {},
        name    = 'story_list',
    ),
    url(
        regex   = '^stories/(?P<story_id>[0-9]+)/$',
        view    = StoryDetailView.as_view(),
        kwargs  = {},
        name    = 'api_stories_detail',
    ),
    url(
        regex   = '^api/stories/$',
        view    = api.as_view(),
        kwargs  = {},
        name    = 'api_stories_list',
    ),
    url(
        regex   = '^api/stories/(?P<story_id>[0-9]+)/$',
        view    = api.as_view(),
        kwargs  = {},
        name    = 'api_stories_detail',
    ),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
