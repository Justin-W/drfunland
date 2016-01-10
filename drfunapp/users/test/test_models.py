from django.test import TestCase
from nose.tools import eq_
from ..models import User


class TestUserModel(TestCase):
    """
    Tests the User model.
    """

    def setUp(self):
        self.username = 'aAardvark'
        self.first_name = 'Aaron'
        self.last_name = 'Aardvark'
        self.password = 'zebra'
        self.user = User.objects.create(username=self.username, password=self.password, first_name=self.first_name,
                                        last_name=self.last_name)

    def test_magic_repr(self):
        expected = '<User: {}>'.format(self.username)
        eq_(self.user.__repr__(), expected)
        eq_(repr(self.user), expected)

    def test_magic_str(self):
        expected = self.username
        eq_(self.user.__str__(), expected)
        eq_(str(self.user), expected)

    def test_magic_unicode(self):
        # user = UserFactory.build()
        expected = self.username
        eq_(self.user.__unicode__(), expected)
        eq_(unicode(self.user), expected)
