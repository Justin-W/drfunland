from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.httpbin_root, name='httpbin_root'),
    url(r'^helloworld', views.hello_world_view, name='helloworld'),
    url(r'^hello', views.hello_world_view, name='hello'),
    url(r'^image', views.httpbin_image, name='httpbin_image'),
    url(r'^text', views.httpbin_text, name='httpbin_text'),
]
