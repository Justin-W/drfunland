from django.core.urlresolvers import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase

from ..views import echo_root, echo_view


class TestApiRootView(APITestCase):
    """
    Tests the / endpoint.
    """

    def setUp(self):
        self.url = reverse(echo_root)
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
            "{'echo_root': 'http://testserver/api/v1/echo/', 'EchoView': 'http://testserver/api/v1/echo/echo'}")  # noqa


class TestEchoView(APITestCase):
    """
    Tests the /echo endpoint.
    """

    def setUp(self):
        self.url = reverse(echo_view)
        # self.url = reverse('echo')
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
        expected = _encode_request_data(self.test_data_in)
        eq_(_decode_response_data(response), expected)

    def test_post_request_expected_data(self):
        response = self.client.post(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        expected = _encode_request_data(self.test_data_in)
        eq_(_decode_response_data(response), expected)


def _decode_response_data(response):
    if response is None:
        return None

    data = response.data
    if type(data) is dict:
        return data

    return _qdict_to_dict(data)


def _encode_request_data(obj):
    if obj is None:
        return None
    return _unicodeify(obj)
    # return _stringify(obj)


def _qdict_to_dict(qdict):
    """Convert a Django QueryDict to a Python dict.

    Single-value fields are put in directly, and for multi-value fields, a list
    of all values is stored at the field's key.
    """
    # assert isinstance(qdict, (django.http.QueryDict, django.http.request.QueryDict))
    try:
        return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}
    except AttributeError:
        return qdict


def _unicodeify(obj):
    """
    Recursively convert a <list> or <dict> object's inner elements to unicode.

    This can be used to simulate the way that non-unicode keys and values in a Request's params or data are
    automatically converted to unicode during the HTTP Request/Response interaction.
    """
    if obj is None:
        return None
    elif isinstance(obj, dict):
        return {_unicodeify(key): _unicodeify(value) for key, value in obj.iteritems()}
    elif isinstance(obj, list):
        return [_unicodeify(element) for element in obj]
    elif isinstance(obj, unicode):
        return obj
    else:
        return unicode(obj)
