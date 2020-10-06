from django.contrib import admin
from .models import Tweet
from .models import Tweet_author

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Tweet_author)