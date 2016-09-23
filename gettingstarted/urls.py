from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^registercoder', hello.views.registerCoder, name='registercoder'),
    url(r'^registerhelper', hello.views.registerHelper, name='registerhelper'),
    url(r'^login', hello.views.user_login, name='user_login'),
    url(r'^home', hello.views.post_login, name='post_login'),
    url(r'^invalidlogin', hello.views.invalidLogin, name='invalidLogin'),
]
