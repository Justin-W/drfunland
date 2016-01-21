from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transitionsfbv_root, name='transitionsfbv_root'),
    url(r'^machines/$', views.transitionsfbv_machines_root, name='transitionsfbv_machines_root'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/$', views.transitionsfbv_machines_pk,
        name='transitionsfbv_machines_pk'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/blueprint/$', views.transitionsfbv_machines_pk_blueprint,
        name='transitionsfbv_machines_pk_blueprint'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph/$', views.transitionsfbv_machines_pk_graph,
    #     name='transitionsfbv_machines_pk_graph'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>(|png|jpeg|svg|dot)))?/$', views.transitionsfbv_machines_pk_graph,
    #     name='transitionsfbv_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>([a-zA-Z0-9\.]+)))?/$', views.transitionsfbv_machines_pk_graph,
        name='transitionsfbv_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/transition/$', views.transitionsfbv_machines_pk_transition,
        name='transitionsfbv_machines_pk_transition'),
]
