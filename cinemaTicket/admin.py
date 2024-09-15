from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CinemaRoom)
admin.site.register(Projection)
admin.site.register(Movie)
admin.site.register(Ticket)
admin.site.register(ValidEmail)
