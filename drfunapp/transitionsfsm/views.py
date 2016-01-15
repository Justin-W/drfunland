from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

import utils

_machine_catalog = utils.MachineCatalog()
_machine_catalog.preload(auto_transitions=False, ignore_invalid_triggers=False)


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_root(request, format=None):
    return Response({
        'transitionsfsm_root': reverse('transitionsfsm_root', request=request, format=format),
        'transitionsfsm_machines_root': reverse('transitionsfsm_machines_root', request=request, format=format),
        'transitionsfsm_machines_pk': reverse('transitionsfsm_machines_pk',
                                              request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_pk_blueprint': reverse('transitionsfsm_machines_pk_blueprint',
                                                        request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_pk_graph': reverse('transitionsfsm_machines_pk_graph',
                                                    request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_pk_transition': reverse('transitionsfsm_machines_pk_transition',
                                                         request=request, format=format, args=('matter',)),
        # 'transitionsfsm_one': reverse('transitionsfsm_one', request=request, format=format),
        # 'transitionsfsm_two': reverse('transitionsfsm_two', request=request, format=format),
        # 'transitionsfsm_image': reverse(transitionsfsm_image, request=request, format=format),
        # 'transitionsfsm_text': reverse(transitionsfsm_text, request=request, format=format),
        # 'hello_world_view': (reverse('transitionsfsm_helloworld', request=request, format=format),
        #                      reverse('transitionsfsm_hello', request=request, format=format))
    })


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_root(request):
    if request.method == 'GET':
        # data = {k: summarize_machine(m, machine_name=k, request=request) for k, m in _machine_catalog.items()}
        data = {k: dict(get_machine_detail_urls(machine_name=k, request=request)) for k, m in _machine_catalog.items()}
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        data = summarize_machine(m, machine_name=pk, request=request)
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk_blueprint(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        data = summarize_machine(m, machine_name=pk, request=request).get('blueprints')
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk_graph(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        return generate_image_response_png(m)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk_transition(request, pk):
    # if request.method == 'GET':
    #     m = _machine_catalog.get(pk)
    #     data = summarize_machine(m, machine_name=pk, request=request)
    #     return Response(data)
    # elif request.method == 'POST':
    #     pass
    #
    return Response('Not yet implemented')


def summarize_machine(m, machine_name, request):
    d = {'_URLS': get_machine_detail_urls(machine_name, request)}
    d.update(utils.summarize_machine(m))
    return d


def get_machine_detail_urls(machine_name, request):
    return [
        ('detail', reverse('transitionsfsm_machines_pk', request=request, args=(machine_name,))),
        ('graph', reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name,))),
        ('blueprint', reverse('transitionsfsm_machines_pk_blueprint', request=request, args=(machine_name,))),
        ('transition', reverse('transitionsfsm_machines_pk_transition', request=request, args=(machine_name,))),
    ]


def generate_image_response_png(machine):
    from django.http import HttpResponse as DjangoHttpResponse

    png = utils.graph_machine(machine, image_format='png', layout_program='dot')
    return DjangoHttpResponse(png, content_type='image/png')
