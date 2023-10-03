from django.urls import path
from .views import UserRegistrationView, ObtainTokenPairView, RefreshTokenView,UserRegistrationSuperuserView

urlpatterns = [
    path("register/",UserRegistrationView.as_view(),name='register'),
    path("register/admin",UserRegistrationSuperuserView.as_view(),name="register_admin"),
    path("token",ObtainTokenPairView.as_view(),name='token_obtain_pair'),
    path("token/refresh",RefreshTokenView.as_view(),name="token_refresh")
]