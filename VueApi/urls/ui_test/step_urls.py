from django.conf.urls import url
from VueApi.views.ui_test import step

urlpatterns = [
    url(r'^$', step.get_step),
    url(r'^/idstep$', step.get_id_step),
    url(r'^/addstep$', step.add_step),
    url(r'^/editstep$', step.edit_step),
    url(r'^/delete', step.delete)
]