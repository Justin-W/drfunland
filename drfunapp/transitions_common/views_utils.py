import ast
# import logging

from rest_framework import serializers
from rest_framework.reverse import reverse
from transitions_common.transitions_extensions import Machine as Machine

from transitions_common import utils
# from transitions_common.utils import LogUtils

_machine_catalog = utils.MachineCatalog()
_machine_catalog.preload(auto_transitions=False, ignore_invalid_triggers=False)


def get_machine_catalog():
    return _machine_catalog


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


def create_machine(states, transitions=None, initial=None, order=None, options=None):
    if not states:
        raise serializers.ValidationError("Invalid value: '{}'".format('states'))
    if not transitions:
        transitions = []
        # raise serializers.ValidationError("Invalid value: '{}'".format('transitions'))
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


def get_machine_detail_dom(m, machine_name, request):
    urls_ = get_machine_detail_urls(machine_name, request)
    d = {}
    d['_URLS'] = urls_
    # d['snapshot(verbose=True)'] = m.snapshot(verbose=True)
    d['snapshot'] = m.snapshot(verbose=False)
    d['summary'] = m.summarize()
    return d


def get_machine_detail_urls(machine_name, request):
    pk = machine_name
    pk_graph_view = 'transitionsfbv_machines_pk_graph'
    return [
        ('detail', reverse('transitionsfbv_machines_pk', request=request, args=(pk,))),
        ('graph', [
            reverse(pk_graph_view, request=request, args=(pk,)),
            {
                'dot': reverse(pk_graph_view, request=request, args=(pk, '.dot')),
                'xdot': reverse(pk_graph_view, request=request, args=(pk, '.xdot')),
                'xdot1.4': reverse(pk_graph_view, request=request, args=(pk, '.xdot1.4')),
                'jpeg': reverse(pk_graph_view, request=request, args=(pk, '.jpeg')),
                'png': reverse(pk_graph_view, request=request, args=(pk, '.png')),
                'svg': reverse(pk_graph_view, request=request, args=(pk, '.svg')),
                'pdf': reverse(pk_graph_view, request=request, args=(pk, '.pdf'))
            }]),
        ('blueprint', reverse('transitionsfbv_machines_pk_blueprint', request=request, args=(pk,))),
        ('snapshot', reverse('transitionsfbv_machines_pk_snapshot', request=request, args=(pk,))),
        ('transition', reverse('transitionsfbv_machines_pk_transition', request=request, args=(pk,))),
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
