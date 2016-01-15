from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
import requests as r4h
import utils

_machine_catalog = utils.MachineCatalog()
_machine_catalog.preload(auto_transitions=False, ignore_invalid_triggers=False)


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_root(request, format=None):
    return Response({
        'transitionsfsm_root': reverse('transitionsfsm_root', request=request, format=format),
        'transitionsfsm_machines_list': reverse('transitionsfsm_machines_list', request=request, format=format),
        'transitionsfsm_machines_detail': reverse('transitionsfsm_machines_detail',
                                                  request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_detail_blueprint': reverse('transitionsfsm_machines_detail_blueprint',
                                                            request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_detail_graph': reverse('transitionsfsm_machines_detail_graph',
                                                        request=request, format=format, args=('matter',)),
        'transitionsfsm_machines_detail_transition': reverse('transitionsfsm_machines_detail_transition',
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
def transitionsfsm_machines_list(request):
    if request.method == 'GET':
        # data = {k: summarize_machine(m, machine_name=k, request=request) for k, m in _machine_catalog.items()}
        data = {k: dict(get_machine_detail_urls(machine_name=k, request=request)) for k, m in _machine_catalog.items()}
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_detail(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        data = summarize_machine(m, machine_name=pk, request=request)
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_detail_blueprint(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        data = summarize_machine(m, machine_name=pk, request=request).get('blueprints')
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_detail_graph(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        return generate_image_response_png(m)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_detail_transition(request, pk):
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
        ('detail', reverse('transitionsfsm_machines_detail', request=request, args=(machine_name,))),
        ('graph', reverse('transitionsfsm_machines_detail_graph', request=request, args=(machine_name,))),
        ('blueprint', reverse('transitionsfsm_machines_detail_blueprint', request=request, args=(machine_name,))),
        ('transition', reverse('transitionsfsm_machines_detail_transition', request=request, args=(machine_name,))),
    ]


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_one(request, format=None):
    machine_name = request.query_params.get('machine', 'a')
    machine = _machine_catalog.create_sample_machine(name=machine_name, auto_transitions=False,
                                                     ignore_invalid_triggers=False)
    return generate_image_response_png(machine)


def generate_image_response_png(machine):
    from django.http import HttpResponse as DjangoHttpResponse

    png = utils.graph_machine(machine, image_format='png', layout_program='dot')
    return DjangoHttpResponse(png, content_type='image/png')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_two(request, format=None):
    return Response('Not yet implemented')


@api_view(['GET', 'POST', ])
@permission_classes((AllowAny,))
def hello_world_view(request):
    if request.method == 'POST':
        data = request.data
    else:
        data = request.query_params
    # data = request.data if request.method == 'POST' else request.query_params
    return Response(data={'message': 'Hello, world!', 'data': data, 'method': request.method})


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_image(request):
    """
    A view that acts as a consolidated facade for several different endpoints at httpbin.org.

    Wrapped endpoints:
        /image Returns page containing an image based on sent Accept header.
        /image/png Returns page containing a PNG image.
        /image/jpeg Returns page containing a JPEG image.
        /image/webp Returns page containing a WEBP image.
        /image/svg Returns page containing a SVG image.
    """
    image_format = request.query_params.get('ext')
    if not image_format:
        url = 'http://httpbin.org/image'
        return _redirect(url)
    # else:

    image_format = str(image_format).lower()
    if image_format in ('jpeg', 'png', 'svg', 'webp'):
        url = 'http://httpbin.org/image/{filetype}'.format(filetype=image_format)
        return _redirect(url)
    else:
        raise serializers.ValidationError('Unsupported image format')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_text(request):
    """
    A view that acts as a consolidated facade for several different endpoints at httpbin.org.

    Wrapped endpoints:
        /get Returns GET data.
        /encoding/utf8 Returns page containing UTF-8 data.
        /html Renders an HTML Page.
        /robots.txt Returns some robots.txt rules.
        /xml Returns some XML
    """
    text_format = request.query_params.get('ext')
    if not text_format:
        text_format = 'json'
    # else:

    text_format = str(text_format).lower()
    if text_format in ('html', 'xml'):
        url = 'http://httpbin.org/{format}'.format(format=text_format)
    elif text_format == 'json':
        url = 'http://httpbin.org/get'
    elif text_format == 'txt':
        url = 'http://httpbin.org/robots.txt'
    elif text_format == 'utf8':
        url = 'http://httpbin.org/encoding/utf8'
    else:
        url = None

    if url:
        response = r4h.get(url)
        return Response(response.content)
    else:
        raise serializers.ValidationError('Unsupported text format')


def _redirect(url):
    headers = {'Location': url}
    return Response(status=status.HTTP_307_TEMPORARY_REDIRECT, headers=headers)
