from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.echo_root, name='echo_root'),
    url(r'^echo$', views.echo_view, name='echo'),
]
