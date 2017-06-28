from django.conf.urls import url
from . import views
app_name = 'login'
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^main$', views.main, name='main'),
    url('^login$', views.login, name='login'),
    url('^register$', views.register, name='register'),
    url('^logout$', views.logout, name='logout'),
]
