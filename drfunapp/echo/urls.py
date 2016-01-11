from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.echo_view, name='echo'),
]
