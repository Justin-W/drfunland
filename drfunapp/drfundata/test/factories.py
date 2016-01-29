import factory


class WebResourceTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'drfundata.WebResourceType'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'testWebResourceType{}'.format(n))
    description = factory.Faker('description')


class WebResourceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'drfundata.WebResource'
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: 'testWebResource{}'.format(n))
    description = factory.Faker('description')
    resource_type = factory.Faker('resource_type')
    uri = factory.Faker('uri')
