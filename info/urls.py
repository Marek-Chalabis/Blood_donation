from django.urls import path

from .views import (PatientCreateView, PatientDetailView, PatientListView,
                    PatientUpdateView, blood_donation, donate, info_branch,
                    info_donor, info_main)

urlpatterns = [
    path("", info_main, name="main"),
    path("branch-informations/<str:branch>", info_branch, name="info-branch"),
    path("donor-informations/", info_donor, name="info-donor"),
    path("donate/", donate, name="donate"),
    path("donate/<int:donor_id>/", blood_donation, name="blood-donation"),
    path("donors/", PatientListView.as_view(), name="patient-home"),
    path("donors/<int:pk>", PatientDetailView.as_view(), name="patient-detail"),
    path("donors/new/", PatientCreateView.as_view(), name="patient-create"),
    path("donors/<int:pk>/update/", PatientUpdateView.as_view(), name="patient-update"),
]
