from rest_framework import parsers, renderers
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


class EchoView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    # serializer_class = AuthTokenSerializer

    # @api_view(['GET', ])
    def get(self, request, *args, **kwargs):
        return Response(data=request.query_params)

    # @api_view(['POST', ])
    def post(self, request, *args, **kwargs):
        return Response(data=request.data)


echo_view = EchoView.as_view()
# echo_view = EchoView.as_view({
#     'get': 'get',
#     'post': 'post'
# })
