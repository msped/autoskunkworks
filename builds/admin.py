from django.contrib import admin
from .models import ExteriorCategory, EngineCategory, InteriorCategory, RunningCategory, Domains

# Register your models here.

admin.site.register(ExteriorCategory)
admin.site.register(EngineCategory)
admin.site.register(InteriorCategory)
admin.site.register(RunningCategory)
admin.site.register(Domains)
