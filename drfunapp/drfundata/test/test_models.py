from django.test import TestCase
from nose.tools import eq_, ok_
from ..models import WebResourceType, WebResource


class TestWebResourceTypeModel(TestCase):
    """
    Tests the WebResourceType model.

    Note: These tests currently do not affect the code coverage metrics, due to django-nose Issue #108.
    However, they do still provide effective protection against functional regression.
    See: https://github.com/django-nose/django-nose/issues/180
    """

    def setUp(self):
        self.name = 'name01'
        self.description = 'description01'
        self.instance = WebResourceType.objects.create(name=self.name, description=self.description)

    def test_magic_repr(self):
        expected = '<WebResourceType: {}>'.format(self.name)
        eq_(self.instance.__repr__(), expected)
        eq_(repr(self.instance), expected)

    def test_magic_str(self):
        expected = self.name
        eq_(self.instance.__str__(), expected)
        eq_(str(self.instance), expected)

    def test_magic_unicode(self):
        # instance = WebResourceTypeFactory.build()
        expected = self.name
        eq_(self.instance.__unicode__(), expected)
        eq_(unicode(self.instance), expected)


class TestWebResourceModel(TestCase):
    """
    Tests the WebResource model.

    Note: See [Making queries](https://docs.djangoproject.com/en/1.9/topics/db/queries/)
    for more details.
    """

    fixtures = ['testdata']

    def setUp(self):
        self.name = 'name01'
        self.description = 'description01'
        self.uri = 'http://www.{}.com'.format(self.name)
        self.resource_type = WebResourceType.objects.first()
        self.instance = WebResource.objects.create(name=self.name, description=self.description, uri=self.uri,
                                                   resource_type=self.resource_type)

    def test_magic_repr(self):
        expected = '<WebResource: {}>'.format(self.name)
        eq_(self.instance.__repr__(), expected)
        eq_(repr(self.instance), expected)

    def test_magic_str(self):
        expected = self.name
        eq_(self.instance.__str__(), expected)
        eq_(str(self.instance), expected)

    def test_magic_unicode(self):
        # instance = WebResourceFactory.build()
        expected = self.name
        eq_(self.instance.__unicode__(), expected)
        eq_(unicode(self.instance), expected)

    def test_fk_resource_type(self):
        expected = self.resource_type.name
        eq_(self.instance.resource_type.name, expected)
        ok_(self.instance.resource_type is self.resource_type)

    def test_filter_by_name(self):
        parent_name = 'Wiki'
        child_name = 'Wikipedia'
        qs = WebResource.objects.filter(name=child_name)
        eq_(len(qs), 1)
        obj = qs.first()
        eq_(obj.name, child_name)
        eq_(obj.resource_type.name, parent_name)

    def test_filter_by_resource_type_name(self):
        parent_name = 'Wiki'
        child_name = 'Wikipedia'
        qs = WebResource.objects.filter(resource_type__name=parent_name)
        eq_(len(qs), 1)
        obj = qs.first()
        eq_(obj.name, child_name)
        eq_(obj.resource_type.name, parent_name)

    def test_filter_by_resource_type_name_sw(self):
        qs = WebResource.objects.filter(resource_type__name__startswith='Web ').order_by('-name')
        eq_(len(qs), 2)
        obj = qs[0]
        parent_name = 'Web Page'
        child_name = 'repl.it/languages'
        eq_(obj.name, child_name)
        eq_(obj.resource_type.name, parent_name)
        obj = qs[1]
        parent_name = 'Web Site'
        child_name = 'repl.it'
        eq_(obj.name, child_name)
        eq_(obj.resource_type.name, parent_name)

    def test_filter_chained(self):
        qs1 = WebResource.objects.all()
        qs2 = qs1.filter(resource_type__name__startswith='Web ')
        qs3 = qs2.exclude(resource_type__name__endswith='ZZZ')
        qs4 = qs3.exclude(resource_type__name__endswith='ge')
        qs5 = qs4.exclude(resource_type__name__contains='P')
        qs6 = qs5.order_by('-name')
        qs7 = qs1.filter(resource_type__name__startswith='ZZZ')
        qs8 = qs1.filter(resource_type__name__endswith='ZZZ')

        qs = qs1
        ok_(len(qs) >= 6)

        qs = qs2
        eq_(len(qs), 2)

        qs = qs7
        eq_(len(qs), 0)

        qs = qs8
        eq_(len(qs), 0)

        qs = qs6
        eq_(len(qs), 1)
        obj = qs[0]
        # parent_name = 'Web Page'
        # child_name = 'repl.it/languages'
        # eq_(obj.name, child_name)
        # eq_(obj.resource_type.name, parent_name)
        # obj = qs[1]
        parent_name = 'Web Site'
        child_name = 'repl.it'
        eq_(obj.name, child_name)
        eq_(obj.resource_type.name, parent_name)
