from django.core.urlresolvers import reverse
from nose.tools import eq_
from rest_framework.test import APITestCase

from ..views import echo_view


class TestEchoView(APITestCase):
    """
    Tests the /echo endpoint.
    """

    def setUp(self):
        self.url = reverse(echo_view)
        self.test_data_in = {'string': 'abc', 'number': 123, 'bool': True, 'list': ['a', 2, 'c']}

    def test_get_request_succeeds(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

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
        eq_(_qdict_to_dict(response.data), expected)

    def test_post_request_expected_data(self):
        response = self.client.post(self.url, data=self.test_data_in)
        eq_(response.status_code, 200)
        expected = _encode_request_data(self.test_data_in)
        eq_(_decode_response_data(response), expected)


def _decode_response_data(response):
    # return response.data
    return _qdict_to_dict(response.data)
    # return _byteify(response.data)
    # return _byteify(_qdict_to_dict(response.data))


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
    return {k: v[0] if len(v) == 1 else v for k, v in qdict.lists()}


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
