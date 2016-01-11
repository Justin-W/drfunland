from rest_framework import parsers, renderers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(('GET',))
@permission_classes((AllowAny,))
def echo_root(request, format=None):
    return Response({
        'echo_root': reverse('echo_root', request=request, format=format),
        'EchoView': reverse('echo', request=request, format=format)
    })


class EchoView(APIView):
    throttle_classes = ()
    permission_classes = (AllowAny,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(data=request.query_params)

    def post(self, request, *args, **kwargs):
        return Response(data=request.data)


echo_view = EchoView.as_view()
