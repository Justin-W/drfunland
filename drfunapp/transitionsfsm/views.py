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
        data = get_machine_list(request)
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


def get_machine_list(request):
    mc = _machine_catalog
    # data = {k: summarize_machine(m, machine_name=k, request=request) for k, m in mc.items()}
    # data = {k: dict(get_machine_detail_urls(machine_name=k, request=request)) for k, m in mc.items()}
    # data = [(k, dict(get_machine_detail_urls(machine_name=k, request=request))) for k, m in mc.items()]
    # data = [{k: dict(get_machine_detail_urls(machine_name=k, request=request))} for k, m in mc.items()]
    # data = tuple([(k, dict(get_machine_detail_urls(machine_name=k, request=request))) for k, m in mc.items()])
    keys = sorted(mc.keys())
    # pairs = [(k, mc[k]) for k in keys]
    # data = [{k: dict(get_machine_detail_urls(machine_name=k, request=request))} for k in keys]
    data = [{'id': k, 'urls': dict(get_machine_detail_urls(machine_name=k, request=request))} for k in keys]
    return data


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
def transitionsfsm_machines_pk_graph(request, pk, ext=None):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        image_format = str(ext or '').lower()
        return create_graphviz_graph_response(m, title=pk, image_format=image_format)
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
    # d.update(utils.summarize_machine(m))
    d.update(m.summarize())
    return d


def get_machine_detail_urls(machine_name, request):
    return [
        ('detail', reverse('transitionsfsm_machines_pk', request=request, args=(machine_name,))),
        ('graph', [
            reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name,)),
            {
                'dot': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.dot')),
                'xdot': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.xdot')),
                'xdot1.4': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.xdot1.4')),  # noqa
                'jpeg': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.jpeg')),
                'png': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.png')),
                'svg': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.svg')),
                'pdf': reverse('transitionsfsm_machines_pk_graph', request=request, args=(machine_name, '.pdf'))
            }]),
        ('blueprint', reverse('transitionsfsm_machines_pk_blueprint', request=request, args=(machine_name,))),
        # ('transition', reverse('transitionsfsm_machines_pk_transition', request=request, args=(machine_name,))),
    ]


def create_graphviz_graph_response(machine, title=None, image_format=None):
    from django.http import HttpResponse as DjangoHttpResponse

    image_format = image_format or 'png'
    data = utils.graph_machine(machine, title=title, image_format=image_format, layout_program='dot')
    content_type = utils.MimeUtils.get_mime_type(image_format)

    if content_type == 'text/plain':
        # return Response(data)
        # return Response(data, content_type=content_type)
        return DjangoHttpResponse(data, content_type=content_type)
    else:
        return DjangoHttpResponse(data, content_type=content_type)
