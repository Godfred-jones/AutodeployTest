from django.urls.conf import include, path

app_name = "api"

urlpatterns = (path("", include("applications.users.urls")),)
