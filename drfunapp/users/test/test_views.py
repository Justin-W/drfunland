from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from faker import Faker
from ..models import User
from .factories import UserFactory

fake = Faker()


class TestUserAPI(APITestCase):
    """
    Tests the /users endpoint.
    """

    def setUp(self):
        self.url = reverse('user-list')
        self.user_data = model_to_dict(UserFactory.build())

    def test_get_request_fails(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 405)

    def test_options_request_succeeds(self):
        response = self.client.options(self.url)
        eq_(response.status_code, 200)

    def test_options_request_expected_data(self):
        response = self.client.options(self.url)
        expected = OrderedDict([(u'name', u'User List'), (u'description', u'Creates, Updates, and retrieves User accounts'), (u'renders', [u'application/json', u'text/html']), (u'parses', [u'application/json', u'application/x-www-form-urlencoded', u'multipart/form-data']), (u'actions', {u'POST': OrderedDict([('id', OrderedDict([(u'type', u'integer'), (u'required', False), (u'read_only', True), (u'label', u'ID')])), ('username', OrderedDict([(u'type', u'string'), (u'required', False), (u'read_only', True), (u'label', u'Username'), (u'help_text', u'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')])), ('first_name', OrderedDict([(u'type', u'string'), (u'required', False), (u'read_only', False), (u'label', u'First name'), (u'max_length', 30)])), ('last_name', OrderedDict([(u'type', u'string'), (u'required', False), (u'read_only', False), (u'label', u'Last name'), (u'max_length', 30)]))])})])  # noqa
        eq_(response.data, expected)

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, 400)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        eq_(response.status_code, 201)

        user = User.objects.get(pk=response.data.get('id'))
        eq_(user.username, self.user_data.get('username'))
        ok_(check_password(self.user_data.get('password'), user.password))


class TestUserDetailAPI(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.user.auth_token))

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        eq_(response.status_code, 200)

    def test_put_request_updates_a_user(self):
        new_first_name = fake.first_name()
        payload = {'first_name': new_first_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, 200)

        user = User.objects.get(pk=self.user.id)
        eq_(user.first_name, new_first_name)
