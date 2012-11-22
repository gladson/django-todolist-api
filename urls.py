from django.conf.urls import patterns, include, url
from tastypie.api import Api
from todolist.api import ListResource, ItemResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ListResource())
v1_api.register(ItemResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_todolist_api.views.home', name='home'),
    # url(r'^django_todolist_api/', include('django_todolist_api.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
