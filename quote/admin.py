from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Import models
from .models import Quote, Author, User, UserProfile, Follow, Like, Comment


"""Register models - creates admin interface for models"""
# admin.site.register(Quote)
# admin.site.register(Author)

"""ModelAdmin subclass customizes the admin interface"""

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'author', 'timestamp')
    search_fields = ['user__username', 'text', 'author__name']
    list_filter = ('timestamp', 'author', 'categories')
    ordering = ['-timestamp']
admin.site.register(Quote, QuoteAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    search_fields = ['name']
    fields = [('name', 'bio'), 'image']
    ordering = ['name']
admin.site.register(Author, AuthorAdmin)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Unregister User model if it's registered
if User in admin.site._registry:
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country_of_origin', 'birthday')
    search_fields = ['user__username', 'country_of_origin']
    ordering = ['user']

admin.site.register(UserProfile, UserProfileAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'timestamp')

admin.site.register(Follow, FollowAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'quote', 'comment', 'author', 'timestamp')

admin.site.register(Like, LikeAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'quote', 'text', 'timestamp')
    search_fields = ['user__username', 'text']
    list_filter = ('timestamp',)
    ordering = ['-timestamp']

admin.site.register(Comment, CommentAdmin)