from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # only if you need to support Python 2
class CommonEntityFieldsModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, )
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class WebResourceType(CommonEntityFieldsModel):
    class Meta:
        verbose_name = "Web Resource Type"


class WebResource(CommonEntityFieldsModel):
    class Meta:
        verbose_name = "Web Resource"

    resource_type = models.ForeignKey(WebResourceType, on_delete=models.PROTECT,
                                      verbose_name="Resource Type")
    # Note: see [Max URI length is effectively 2047](http://stackoverflow.com/a/417184)
    uri = models.URLField(max_length=2000)
    # Note: We could instead use a TextField (instead of URLField which is a CharField) like this:
    # from django.core.validators import URLValidator
    # uri = models.TextField(max_length=2000, validators=[URLValidator()])


# class ArcService(CommonEntityFieldsModel):
#     pass


# class ArcClient(CommonEntityFieldsModel):
#     pass


# class ArcProject(CommonEntityFieldsModel):
#     pass
