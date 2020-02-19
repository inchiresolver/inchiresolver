from django.contrib import admin
from .models import InChI, Organization

# Register your models here.



@admin.register(InChI)
class InchiAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass