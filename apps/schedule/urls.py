from django.conf.urls import url
from . import views
app_name = 'schedule'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<appt>\d+)$', views.edit, name='edit'),
    url(r'^add$', views.add, name='add'),
    url(r'^delete/(?P<appt>\d+)$', views.delete, name='delete'),
    url(r'^update/(?P<appt>\d+)$', views.update, name='update'),
]