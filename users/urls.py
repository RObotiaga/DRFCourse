from django.urls import path
from .views import UserUpdateAPIView, UserRetrieveAPIView, \
    UserCreateAPIView, CustomTokenObtainPairView
from .apps import UsersConfig
from rest_framework_simplejwt.views \
    import TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path('edit/<int:pk>/', UserUpdateAPIView.as_view(),
         name='edit-user'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(),
         name='view-user'),
    path('register/', UserCreateAPIView.as_view(),
         name='create-user'),
    path('token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
