from django.contrib import admin
from .models import Skill, Developer, Message, User
# Register your models here.

admin.site.register(User)
admin.site.register(Developer)
admin.site.register(Skill)
admin.site.register(Message)
