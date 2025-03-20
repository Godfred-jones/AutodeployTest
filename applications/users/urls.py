from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

app_name = "users"

if settings.DEBUG:
    user_router = DefaultRouter()
    create_user_router = DefaultRouter()
    login_activity_router = DefaultRouter()
else:
    user_router = SimpleRouter()
    create_user_router = SimpleRouter()
    login_activity_router = SimpleRouter()


# create_user_router.register("", CreateUserView, basename="create-user")

# user_router.register("", CustomDjoserViewSet, basename="users")

# login_activity_router.register("", LoginActivityView, basename="login-activity")

urlpatterns = [
    path("users/", include("djoser.urls.authtoken")),
]
