from django.contrib import admin
from django.core import urlresolvers
from .models import WebResource, WebResourceType


# Register your models here.

class CommonEntityFieldsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fieldsets = (
        # (None, {
        #     'fields': ('name', 'description')
        # }),
        ('Identification Properties', {
            'fields': ('name', 'description')
        }),
    )


@admin.register(WebResourceType)
class WebResourceTypeAdmin(CommonEntityFieldsModelAdmin):
    pass


@admin.register(WebResource)
class WebResourceAdmin(CommonEntityFieldsModelAdmin):
    # list_display = ('name', 'description', 'resource_type', 'resource_type_link', 'uri')
    list_display = ('name', 'description', 'resource_type_link', 'uri')
    fieldsets = CommonEntityFieldsModelAdmin.fieldsets + (
        ('Resource Properties', {
            'fields': ('resource_type', 'uri')
        }),
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': (),
        # }),
    )

    def resource_type_link(self, obj):
        link = urlresolvers.reverse("admin:drfundata_webresourcetype_change", args=[obj.resource_type.id])
        return u'<a href="%s">%s</a>' % (link, obj.resource_type.name)
    resource_type_link.allow_tags = True
    resource_type_link.short_description = WebResource._meta.get_field('resource_type').verbose_name
