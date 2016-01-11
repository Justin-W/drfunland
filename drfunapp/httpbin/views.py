from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
import requests as r4h


@api_view(('GET',))
@permission_classes((AllowAny, ))
def httpbin_root(request, format=None):
    return Response({
        'httpbin_root': reverse('httpbin_root', request=request, format=format),
        'httpbin_image': reverse(httpbin_image, request=request, format=format),
        'httpbin_text': reverse(httpbin_text, request=request, format=format),
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


@api_view(('GET',))
@permission_classes((AllowAny, ))
def httpbin_image(request):
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
@permission_classes((AllowAny, ))
def httpbin_text(request):
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
