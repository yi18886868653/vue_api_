from django.conf.urls import url
from VueApi.views.ui_test import element_page

urlpatterns = [
    url(r'^$', element_page.get_element_page),
    url(r'^/addelementpage$', element_page.add_element_page),
    url(r'^/idelementpage$', element_page.get_id_element_page),
    url(r'^/editelementpage$', element_page.edit_element_page),
    url(r'^/delete', element_page.delete)
]