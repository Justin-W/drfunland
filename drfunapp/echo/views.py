from rest_framework import parsers, renderers
from rest_framework.response import Response
from rest_framework.views import APIView


class EchoView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(data=request.query_params)

    def post(self, request, *args, **kwargs):
        return Response(data=request.data)


echo_view = EchoView.as_view()
