from django.urls import path
from assistant.views import NaturalLanguageQueryView

urlpatterns = [
    path("nl-query/", NaturalLanguageQueryView.as_view(), name="nl-query"),
]