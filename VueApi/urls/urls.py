from django.conf.urls import url, include

from VueApi.views import views

urlpatterns = [
    url(r'^$', views.test),
    url(r'^myapi$', views.my_api),
    url(r'^login$', views.login),
    url(r'^users', include('VueApi.urls.users.user_urls')),
    url(r'^case', include('VueApi.urls.ui_test.case_urls')),
    url(r'^method', include('VueApi.urls.ui_test.method_urls')),
    url(r'^element', include('VueApi.urls.ui_test.element_urls')),
    url(r'^elementpage', include('VueApi.urls.ui_test.element_page_urls')),
    url(r'^step', include('VueApi.urls.ui_test.step_urls')),
    url(r'^record', include('VueApi.urls.ui_test.record_urls'))

]