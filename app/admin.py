from django.contrib import admin
from .models import UserDetail,BlogPost,Category
# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    exclude=['slug','post_image','video','post_title']
    list_display=('id','author','intro','created','updated',)
    list_display_links = ('id', 'author','intro')
    list_per_page=30


admin.site.register(UserDetail)
admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(Category)