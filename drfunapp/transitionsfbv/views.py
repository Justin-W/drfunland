import ast

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from transitions_common.exceptions import RequestedOperationFailedException
from transitions_common.views_utils import add_new_machine_to_catalog, create_graphviz_graph_response, \
    get_machine_catalog, get_machine_list, get_machine_detail_dom


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfbv_root(request, format=None):
    return Response({
        'transitionsfbv_root': reverse('transitionsfbv_root', request=request, format=format),
        'transitionsfbv_machines_root': reverse('transitionsfbv_machines_root', request=request, format=format),
        'transitionsfbv_machines_pk': reverse('transitionsfbv_machines_pk',
                                              request=request, format=format, args=('matter',)),
        'transitionsfbv_machines_pk_blueprint': reverse('transitionsfbv_machines_pk_blueprint',
                                                        request=request, format=format, args=('matter',)),
        'transitionsfbv_machines_pk_graph': reverse('transitionsfbv_machines_pk_graph',
                                                    request=request, format=format, args=('matter',)),
        'transitionsfbv_machines_pk_transition': reverse('transitionsfbv_machines_pk_transition',
                                                         request=request, format=format, args=('matter',)),
    })


@api_view(('GET', 'POST'))
@permission_classes((AllowAny,))
def transitionsfbv_machines_root(request):
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


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfbv_machines_pk(request, pk):
    if request.method == 'GET':
        mc = get_machine_catalog()
        m = mc.get(pk)
        # LogUtils.log_object_state(m.blueprints, level=logging.WARN, name='m.blueprints', context='original')
        # LogUtils.log_object_state(m.snapshot(), level=logging.WARN, name='m.snapshot()', context='original')
        data = get_machine_detail_dom(m, machine_name=pk, request=request)
        return Response(data)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfbv_machines_pk_blueprint(request, pk):
    if request.method == 'GET':
        mc = get_machine_catalog()
        m = mc.get(pk)
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
def transitionsfbv_machines_pk_graph(request, pk, ext=None):
    if request.method == 'GET':
        mc = get_machine_catalog()
        m = mc.get(pk)
        image_format = str(ext or '').lower()
        return create_graphviz_graph_response(m, title=pk, image_format=image_format)
    elif request.method == 'POST':
        pass

    return Response('Not yet implemented')


@api_view(('GET',))
@permission_classes((AllowAny,))
def transitionsfbv_machines_pk_snapshot(request, pk):
    data = request.GET
    mc = get_machine_catalog()
    m = mc.get(pk)
    verbose = bool(ast.literal_eval(data.get('verbose', 'False')))
    data = m.snapshot(verbose=verbose)
    return Response(data)


@api_view(('GET', 'POST',))
@permission_classes((AllowAny,))
def transitionsfbv_machines_pk_transition(request, pk):
    # {"trigger": "evaporate", "dest": "gas"}
    if request.method == 'GET':
        data = request.GET
    elif request.method == 'POST':
        data = request.POST

    mc = get_machine_catalog()
    m = mc.get(pk)
    trigger = data.get('trigger')
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
