from django.conf.urls import patterns, url

urlpatterns = patterns('familytree.views',
    url(r'^$', 'family_member', {'member_id':1}),
    url(r'^(?P<member_id>\d+)/$', 'family_member'),
    url(r'search', 'family_member_search'),
)