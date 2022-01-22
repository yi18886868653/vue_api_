from django.conf.urls import url

from VueApi.views.ui_test import record

urlpatterns = [
    url(r'^$', record.get_record),
    url(r'^/addrecord', record.add_record),
    url(r'^/editrecord', record.edit_record),
    url(r'^/idrecord', record.get_id_record),
    url(r'^/delete',record.delete),
    url(r'^/case',record.case),
    url(r'^/jenkins',record.jenkins)
]