from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserViewSet, UserProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
] + router.urls