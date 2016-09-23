from django.contrib import admin
#from .models import Publisher
# Register your models here.
from .models import Helper
from .models import Coder
admin.site.register(Helper)
admin.site.register(Coder)