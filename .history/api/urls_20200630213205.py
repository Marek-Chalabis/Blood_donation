from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import DonationViewSet, PatientViewSet, PublicInfoViewSet, UserViewSet

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patients")
router.register("donations", DonationViewSet, basename="donations")
router.register("users", UserViewSet, basename="users")
router.register("public", PublicInfoViewSet, basename="public")


urlpatterns = [
    path("v1/", include(router.urls)),
    path("get-token", views.obtain_auth_token),
]
