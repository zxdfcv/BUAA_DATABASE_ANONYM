from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Classification1)
admin.site.register(Classification2)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(LoginLog)
admin.site.register(OpLog)
admin.site.register(ErrorLog)
admin.site.register(Order)
admin.site.register(Chat)
