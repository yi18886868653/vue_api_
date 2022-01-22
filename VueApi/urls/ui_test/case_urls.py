from django.conf.urls import url

from VueApi.views.ui_test import case

urlpatterns = [
    url(r'^$', case.get_case),
    url(r'^/addcase', case.add_case),
    url(r'^/editcase', case.edit_case),
    url(r'^/idcase', case.get_id_case),
    url(r'^/delete',case.delete),
    url(r'^/case',case.case)
]