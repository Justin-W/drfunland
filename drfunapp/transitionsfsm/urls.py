from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transitionsfsm_root, name='transitionsfsm_root'),
    url(r'^helloworld', views.hello_world_view, name='transitionsfsm_helloworld'),
    url(r'^hello', views.hello_world_view, name='transitionsfsm_hello'),
    url(r'^image', views.transitionsfsm_image, name='transitionsfsm_image'),
    url(r'^text', views.transitionsfsm_text, name='transitionsfsm_text'),
    url(r'^one', views.transitionsfsm_one, name='transitionsfsm_one'),
    url(r'^two', views.transitionsfsm_two, name='transitionsfsm_two'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/blueprint', views.transitionsfsm_machines_detail_blueprint,
        name='transitionsfsm_machines_detail_blueprint'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph', views.transitionsfsm_machines_detail_graph,
        name='transitionsfsm_machines_detail_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/transition', views.transitionsfsm_machines_detail_transition,
        name='transitionsfsm_machines_detail_transition'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/', views.transitionsfsm_machines_detail,
        name='transitionsfsm_machines_detail'),
    url(r'^machines/', views.transitionsfsm_machines_list, name='transitionsfsm_machines_list'),
]
