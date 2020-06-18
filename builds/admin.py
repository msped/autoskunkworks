from django.contrib import admin
from .models import ExteriorCategory, EngineCategory, InteriorCategory, RunningCategory

# Register your models here.

admin.site.regsiter(ExteriorCategory)
admin.site.regsiter(EngineCategory)
admin.site.regsiter(InteriorCategory)
admin.site.regsiter(RunningCategory)
