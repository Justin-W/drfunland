from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transitionscbv_root, name='transitionscbv_root'),
    url(r'^machines/$', views.transitionscbv_machines_root, name='transitionscbv_machines_root'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/$', views.transitionscbv_machines_pk,
        name='transitionscbv_machines_pk'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/blueprint/$', views.transitionscbv_machines_pk_blueprint,
        name='transitionscbv_machines_pk_blueprint'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph/$', views.transitionscbv_machines_pk_graph,
    #     name='transitionscbv_machines_pk_graph'),
    # url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>(|png|jpeg|svg|dot)))?/$', views.transitionscbv_machines_pk_graph,
    #     name='transitionscbv_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/graph(\.(?P<ext>([a-zA-Z0-9\.]+)))?/$', views.transitionscbv_machines_pk_graph,
        name='transitionscbv_machines_pk_graph'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/snapshot/$', views.transitionscbv_machines_pk_snapshot,
        name='transitionscbv_machines_pk_snapshot'),
    url(r'^machines/(?P<pk>[a-zA-Z0-9]+)/transition/$', views.transitionscbv_machines_pk_transition,
        name='transitionscbv_machines_pk_transition'),
]
