from django.conf.urls import url
from VueApi.views.ui_test import ui_element

urlpatterns = [
    url(r'^$', ui_element.get_element),
    url(r'^/addelement$', ui_element.add_element),
    url(r'^/idelement$', ui_element.get_id_element),
    url(r'^/editelement$', ui_element.edit_element),
    url(r'^/delete', ui_element.delete),
]