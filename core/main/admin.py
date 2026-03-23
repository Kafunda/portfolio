from django.contrib import admin
from .models import Project, Service, Skill

# Register your models here.


admin.site.register(Project)
admin.site.register(Service)
admin.site.register(Skill)