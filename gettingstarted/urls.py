from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register', hello.views.register, name='register'),
    url(r'^login', hello.views.user_login, name='user_login'),
    url(r'^home', hello.views.post_login, name='post_login'),
    url(r'^invalidlogin', hello.views.invalidLogin, name='invalidLogin'),
    url(r'^test', hello.views.balance_options, name='balance_options'),
]
