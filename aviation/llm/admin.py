from django.contrib import admin
from .models import RoadmapRequest, RoadmapResult

@admin.register(RoadmapRequest)
class RoadmapRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "topic", "created_at")
    search_fields = ("topic", "user__username")

@admin.register(RoadmapResult)
class RoadmapResultAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "created_at")
    readonly_fields = ("response_json",)