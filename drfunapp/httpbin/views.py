from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse


@api_view(('GET',))
@permission_classes((AllowAny, ))
def httpbin_root(request, format=None):
    return Response({
        'httpbin_root': reverse('httpbin_root', request=request, format=format),
        'hello_world_view': (reverse('helloworld', request=request, format=format),
                             reverse('hello', request=request, format=format))
    })


@api_view(['GET', 'POST', ])
@permission_classes((AllowAny, ))
def hello_world_view(request):
    if request.method == 'POST':
        data = request.data
    else:
        data = request.query_params
    # data = request.data if request.method == 'POST' else request.query_params
    return Response(data={'message': 'Hello, world!', 'data': data, 'method': request.method})
