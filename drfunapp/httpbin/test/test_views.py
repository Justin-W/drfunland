from django.core.urlresolvers import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase

from ..views import httpbin_root


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
        eq_(repr(response.data),
            "{'httpbin_root': 'http://testserver/api/v1/httpbin/', 'hello_world_view': ('http://testserver/api/v1/httpbin/helloworld', 'http://testserver/api/v1/httpbin/hello')}")  # noqa


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
