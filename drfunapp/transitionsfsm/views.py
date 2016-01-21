import ast
# import logging

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
# from transitions import Machine
from transitions_extensions import Machine as Machine

from exceptions import RequestedOperationFailedException
import utils
# from utils import LogUtils

_machine_catalog = utils.MachineCatalog()
_machine_catalog.preload(auto_transitions=False, ignore_invalid_triggers=False)


def get_machine_catalog():
    return _machine_catalog


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
    })


@api_view(('GET', 'POST'))
@permission_classes((AllowAny,))
def transitionsfsm_machines_root(request):
    if request.method == 'GET':
        data = get_machine_list(request)
        return Response(data)
    elif request.method == 'POST':
        data = request.data
        m = add_new_machine_to_catalog(data)

        # data = m.summarize()
        data = m.snapshot(verbose=True)
        return Response(data)

    raise MethodNotAllowed()


def add_new_machine_to_catalog(data):
    # LogUtils.log_object_state(data, level=logging.WARN, name='data', context='original')
    data = dict(data)
    # LogUtils.log_object_state(data, level=logging.WARN, name='data', context='converted to dict')
    data = utils.stringify(data)
    # LogUtils.log_object_state(data, level=logging.WARN, name='data', context='stringified')

    # create a new machine from the request data
    name, states, transitions, initial, order, options = parse_new_machine_data(data)
    m = create_machine(states, transitions, initial, order, options)

    # add the new machine to the catalog
    add_machine_to_catalog(name, m)

    return m


def parse_new_machine_data(data):
    name = data.get('name')
    if name:
        # LogUtils.log_object_state(name, level=logging.WARN, name='name', context='original')
        name = name[0]
    states = data.get('states')
    # if states:
    #     LogUtils.log_object_state(states, level=logging.WARN, name='states', context='original')
    #     # states = [x for x in states]
    #     # LogUtils.log_object_state(states, level=logging.WARN, name='states', context='parsed')
    transitions = data.get('transitions')
    if transitions:
        # LogUtils.log_object_state(transitions, level=logging.WARN, name='transitions', context='original')
        # LogUtils.log_object_state(transitions[0], level=logging.WARN, name='transitions[0]', context='original')
        transitions = [ast.literal_eval(x) for x in transitions]
        # LogUtils.log_object_state(transitions, level=logging.WARN, name='transitions', context='parsed')
        # LogUtils.log_object_state(transitions[0], level=logging.WARN, name='transitions[0]', context='parsed')
    initial = data.get('initial')
    if initial:
        # LogUtils.log_object_state(initial, level=logging.WARN, name='initial', context='original')
        initial = initial[0]
        # LogUtils.log_object_state(initial, level=logging.WARN, name='initial', context='parsed')
    order = data.get('order')
    # if order:
    #     LogUtils.log_object_state(order, level=logging.WARN, name='order', context='original')
    options = data.get('options', {})
    # if options:
    #     # LogUtils.log_object_state(options, level=logging.WARN, name='options', context='original')
    return name, states, transitions, initial, order, options


def add_machine_to_catalog(name, machine):
    if not name:
        raise serializers.ValidationError("Invalid value: '{}'".format('name'))
    _machine_catalog[name] = machine


def create_machine(states, transitions, initial, order, options):
    if not states:
        raise serializers.ValidationError("Invalid value: '{}'".format('states'))
    # if not transitions:
    #     raise serializers.ValidationError("Invalid value: '{}'".format('transitions'))
    if not initial:
        initial = states[0]
    options_default = {'auto_transitions': False, 'ignore_invalid_triggers': False}
    if options:
        # LogUtils.log_object_state(options, level=logging.WARN, name='options', context='original')
        options = utils.kwargs_merge(options, options_default)
        # LogUtils.log_object_state(options, level=logging.WARN, name='options', context='parsed')
    else:
        options = options_default
    m = Machine(states=states, transitions=transitions, initial=initial, **options)
    if order:
        m.add_ordered_transitions(order)
    return m


def get_machine_list(request):
    mc = _machine_catalog
    # data = {k: get_machine_detail_dom(m, machine_name=k, request=request) for k, m in mc.items()}
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
        # LogUtils.log_object_state(m.blueprints, level=logging.WARN, name='m.blueprints', context='original')
        # LogUtils.log_object_state(m.snapshot(), level=logging.WARN, name='m.snapshot()', context='original')
        data = get_machine_detail_dom(m, machine_name=pk, request=request)
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk_blueprint(request, pk):
    if request.method == 'GET':
        m = _machine_catalog.get(pk)
        # data = get_machine_detail_dom(m, machine_name=pk, request=request).get('blueprints')
        try:
            bp_ = m.blueprints
        except AttributeError:
            raise RequestedOperationFailedException(detail='The specified Machine does not support blueprints functionality.')
        else:
            data = bp_
        return Response(data)
    elif request.method == 'POST':
        pass

    # return Response('Not yet implemented')
    raise MethodNotAllowed()


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


@api_view(('GET', 'POST',))
@permission_classes((AllowAny,))
def transitionsfsm_machines_pk_transition(request, pk):
    # {"trigger": "evaporate", "dest": "gas"}
    if request.method == 'GET':
        data = request.GET
    elif request.method == 'POST':
        data = request.POST

    m = _machine_catalog.get(pk)
    trigger = data.get('trigger')
    # dest = request.POST.get('destination', 'next_state')
    dest = data.get('destination')

    if not trigger:
        raise serializers.ValidationError("Invalid value: '{}'".format('trigger'))
    if not dest:
        raise serializers.ValidationError("Invalid value: '{}'".format('destination'))

    t = m.trigger_transition(trigger=trigger, dest_state=dest)
    if not t:
        raise RequestedOperationFailedException()
    # data = get_machine_detail_dom(m, machine_name=pk, request=request)
    data = m.snapshot()
    return Response(data)


def get_machine_detail_dom(m, machine_name, request):
    urls_ = get_machine_detail_urls(machine_name, request)
    d = {}
    d['_URLS'] = urls_
    # d['snapshot(verbose=True)'] = m.snapshot(verbose=True)
    d['snapshot'] = m.snapshot(verbose=False)
    d['summary'] = m.summarize()
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
        ('transition', reverse('transitionsfsm_machines_pk_transition', request=request, args=(machine_name,))),
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
