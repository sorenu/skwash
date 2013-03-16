from django.conf.urls import patterns, include, url
from skwash import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/logout/$', 'skwash.apps.website.views.logout'),
    (r'^accounts/', include('registration.backends.default.urls')),
    # (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'', include('skwash.apps.website.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_URL}),
        (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL}),
    )