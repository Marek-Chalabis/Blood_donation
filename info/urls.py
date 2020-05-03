from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import info_main, donate, blood_donation, info_donor, info_branch, \
    PatientCreateView, PatientListView, PatientDetailView, PatientUpdateView

urlpatterns = [
    path('', info_main, name="main"),
    path('branch-informations/<str:branch>', info_branch, name='info-branch'),
    path('donor-informations/', info_donor, name='info-donor'),

    path('donate/', donate, name="donate"),
    path('donate/<int:donor_id>/', blood_donation, name="blood-donation"),

    path('donors/', PatientListView.as_view(), name='patient-home'),
    path('donors/<int:pk>', PatientDetailView.as_view(), name='patient-detail'),
    path('donors/new/', PatientCreateView.as_view(), name="patient-create"),
    path('donors/<int:pk>/update/', PatientUpdateView.as_view(), name='patient-update'),
]
