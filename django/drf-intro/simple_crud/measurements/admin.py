from django.contrib import admin
from .models import Project, Measurement


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass
