from django.contrib import admin

# Register your models here.
from myapp.models import Analysis, File, Sample

admin.site.register(File)
admin.site.register(Analysis)
admin.site.register(Sample)