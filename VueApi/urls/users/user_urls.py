from django.conf.urls import url

from VueApi.views.user import users

urlpatterns = [
    url(r'^$', users.users),
    url(r'menus', users.menus)
]
