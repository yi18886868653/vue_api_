from django.conf.urls import url
from VueApi.views.ui_test import method

urlpatterns = [
    url(r'^$', method.get_method),
    url(r'^/addmethod',method.add_method),
    url(r'^/idmethod',method.get_id_method),
    url(r'^/editmethod',method.edit_methode),
    url(r'^/delete', method.delete),

]