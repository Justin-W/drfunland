from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transitionsfsm_root, name='transitionsfsm_root'),
    url(r'^machines/$', views.transitionsfsm_machines_root, name='transitionsfsm_machines_root'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/$', views.transitionsfsm_machines_pk,
        name='transitionsfsm_machines_pk'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/blueprint/$', views.transitionsfsm_machines_pk_blueprint,
        name='transitionsfsm_machines_pk_blueprint'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph/$', views.transitionsfsm_machines_pk_graph,
    #     name='transitionsfsm_machines_pk_graph'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>(|png|jpeg|svg|dot)))?/$', views.transitionsfsm_machines_pk_graph,
    #     name='transitionsfsm_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>([a-zA-Z0-9\.]+)))?/$', views.transitionsfsm_machines_pk_graph,
        name='transitionsfsm_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/transition/$', views.transitionsfsm_machines_pk_transition,
        name='transitionsfsm_machines_pk_transition'),
]
