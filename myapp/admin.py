from django.contrib import admin
from .models import Post,Comment, SocialMediaLink
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('postname', 'category', 'time', 'likes_count', 'user', 'content', 'social_image', 'social_title', 'meta_description', 'social_description', 'meta_keywords')
    search_fields = ('postname', 'category', 'user__username')
    
    # Add this method
    def likes_count(self, obj):
        return obj.likes.count()
    likes_count.short_description = 'Likes'

    fieldsets = (
        ('Post Info', {
            'fields': ('postname', 'category', 'image', 'content', 'time', 'user')  # Remove 'likes_count' here
        }),
        ('SEO Options', {
            'fields': ('meta_keywords', 'meta_description', 'social_title', 'social_description', 'social_image')
        }),
    )

admin.site.register(Comment)



admin.site.site_header = 'BLOGSPOT | ADMIN PANEL'
admin.site.site_title = 'BLOGSPOT | BLOGGING WEBSITE'
admin.site.index_title= 'BlogSpot Site Administration'

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')


# for visitors

from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from myapp.utils import get_online_user_count

class MyAdminSite(admin.AdminSite):
    site_header = 'Blog Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        online_users = get_online_user_count()
        context = dict(
            self.each_context(request),
            online_users=online_users,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

admin_site = MyAdminSite(name='myadmin')


