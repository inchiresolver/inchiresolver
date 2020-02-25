from django.contrib import admin
from .models import Inchi, Organization

# Register your models here.



@admin.register(Inchi)
class InchiAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass