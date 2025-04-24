from django.contrib import admin
from .models import Post,Comment,Contact, SocialMediaLink
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('postname', 'category', 'time', 'likes', 'user')
    search_fields = ('postname', 'category', 'user__username')
    fieldsets = (
        ('Post Info', {
            'fields': ('postname', 'category', 'image', 'content', 'time', 'likes', 'user')
        }),
        ('SEO Options', {
            'fields': ('meta_keywords', 'meta_description', 'social_title', 'social_description', 'social_image')
        }),
    )
admin.site.register(Comment)
admin.site.register(Contact)



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


