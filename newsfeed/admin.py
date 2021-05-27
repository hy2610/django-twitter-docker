from django.contrib import admin
from newsfeed.models import NewsFeed


@admin.register(NewsFeed)
class NewsFeed(admin.ModelAdmin):
    list_display = ('user', 'tweet', 'created_at')
    date_hierarchy = 'created_at'

# Register your models here.
