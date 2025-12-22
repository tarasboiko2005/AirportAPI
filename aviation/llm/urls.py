from django.urls import path
from .views import RoadmapView

urlpatterns = [
    path("roadmap", RoadmapView.as_view(), name="llm-roadmap"),
]