from django.core.urlresolvers import reverse
from nose.tools import eq_, ok_
from rest_framework.test import APITestCase

from ..views import httpbin_root, httpbin_image


class TestApiRootView(APITestCase):
    """
    Tests the httpbin_root FBV.
    """

    def setUp(self):
        self.url = reverse(httpbin_root)
        self.test_data_in = {'string': 'abc', 'number': 123, 'bool': True, 'list': ['a', 2, 'c']}

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 405)

    def test_get_request_with_valid_data_succeeds(self):
        response = self.client.get(self.url, self.test_data_in)
        eq_(response.status_code, 200)

    def test_post_request_with_valid_data_fails(self):
        response = self.client.post(self.url, self.test_data_in)
        eq_(response.status_code, 405)

    def test_get_request_expected_data(self):
        response = self.client.get(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        ok_("'httpbin_root': 'http://testserver/api/v1/httpbin/'" in repr(response.data))
        ok_("'httpbin_image': 'http://testserver/api/v1/httpbin/image'" in repr(response.data))
        ok_("'hello_world_view': ('http://testserver/api/v1/httpbin/helloworld', 'http://testserver/api/v1/httpbin/hello')" in repr(response.data))  # noqa


class TestHelloWorldView(APITestCase):
    """
    Tests the hello_world_view FBV.
    """

    def setUp(self):
        self.url = reverse('helloworld')
        self.test_data_in = {'string': 'abc', 'number': 123, 'bool': True, 'list': ['a', 2, 'c']}

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_post_request_with_no_data_succeeds(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 200)

    def test_get_request_with_valid_data_succeeds(self):
        response = self.client.get(self.url, self.test_data_in)
        eq_(response.status_code, 200)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.test_data_in)
        eq_(response.status_code, 200)

    def test_get_request_expected_data(self):
        response = self.client.get(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        eq_(repr(response.data),
            "{'message': 'Hello, world!', 'data': <QueryDict: {u'bool': [u'True'], u'list': [u'a', u'2', u'c'], u'string': [u'abc'], u'number': [u'123']}>, 'method': 'GET'}")  # noqa

    def test_post_request_expected_data(self):
        response = self.client.post(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        eq_(repr(response.data),
            "{'message': 'Hello, world!', 'data': <QueryDict: {u'bool': [u'True'], u'list': [u'a', u'2', u'c'], u'string': [u'abc'], u'number': [u'123']}>, 'method': 'POST'}")  # noqa


class TestHttpbinImageView(APITestCase):
    """
    Tests the httpbin_image FBV.
    """

    def setUp(self):
        self.url = reverse(httpbin_image)

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 307)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_put_request_fails(self):
        response = self.client.put(self.url)
        eq_(response.status_code, 405)

    def test_delete_request_fails(self):
        response = self.client.delete(self.url)
        eq_(response.status_code, 405)

    def test_get_request_with_valid_data_succeeds(self):
        for image_type in ('', 'jpeg', 'png', 'svg', 'webp'):
            response = self.client.get(self.url, {'ext': image_type})
            eq_(response.status_code, 307)

    def test_get_request_with_invalid_data_fails(self):
        for image_type in ('txt', 'xml', 'html', '.'):
            response = self.client.get(self.url, {'ext': image_type})
            eq_(response.status_code, 400)
