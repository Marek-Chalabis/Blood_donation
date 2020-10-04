import pytest
from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer

from info.models import Patient
from info.views import info_main, info_branch, info_donor, donate, blood_donation, PatientListView, PatientDetailView, \
    PatientCreateView, PatientUpdateView


@pytest.mark.django_db
class TestViews:

    def test_info_main(self):
        path = reverse('main')
        request = RequestFactory().get(path)
        response = info_main(request)
        assert response.status_code == 200

    def test_info_branch(self):
        path = reverse('info-branch', kwargs={'branch': 'TEST_brach'})
        request = RequestFactory().get(path)
        response = info_branch(request, branch='TEST_brach')
        assert response.status_code == 200

    def test_info_donor(self):
        path = reverse('info-donor')
        request = RequestFactory().get(path)
        response = info_donor(request)
        assert response.status_code == 200

    def test_donate_authenticated(self):
        path = reverse('donate')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = donate(request)
        assert response.status_code == 200

    def test_donate_unauthenticated(self):
        path = reverse('donate')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = donate(request)
        assert response.status_code == 302
        assert '/login' in response.url

    def test_blood_donation_authenticated(self):
        mixer.blend(Patient)
        path = reverse('blood-donation', kwargs={'donor_id': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = blood_donation(request, donor_id=1)
        assert response.status_code == 200

    def test_blood_donation_unauthenticated(self):
        mixer.blend(Patient)
        path = reverse('blood-donation', kwargs={'donor_id': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = blood_donation(request, donor_id=1)
        assert response.status_code == 302
        assert '/login' in response.url

    def test_PatientListView_authenticated(self):
        path = reverse('patient-home')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = PatientListView.as_view()(request)
        assert response.status_code == 200

    def test_PatientListView_unauthenticated(self):
        path = reverse('patient-home')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = PatientListView.as_view()(request)
        assert response.status_code == 302
        assert '/login' in response.url

    def test_PatientDetailView_authenticated(self):
        mixer.blend(Patient)
        path = reverse('patient-detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = PatientDetailView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_PatientDetailView_unauthenticated(self):
        mixer.blend(Patient)
        path = reverse('patient-detail', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = PatientDetailView.as_view()(request, pk=1)
        assert response.status_code == 302
        assert '/login' in response.url

    def test_PatientCreateView_authenticated(self):
        path = reverse('patient-create')
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = PatientCreateView.as_view()(request)
        assert response.status_code == 200

    def test_PatientCreateView_unauthenticated(self):
        path = reverse('patient-create')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = PatientCreateView.as_view()(request)
        assert response.status_code == 302
        assert '/login' in response.url

    def test_PatientUpdateView_authenticated(self):
        mixer.blend(Patient)
        path = reverse('patient-update', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = mixer.blend(User)
        response = PatientUpdateView.as_view()(request, pk=1)
        assert response.status_code == 200

    def test_PatientUpdateView_unauthenticated(self):
        mixer.blend(Patient)
        path = reverse('patient-update', kwargs={'pk': 1})
        request = RequestFactory().get(path)
        request.user = AnonymousUser()
        response = PatientUpdateView.as_view()(request, pk=1)
        assert response.status_code == 302
        assert '/login' in response.url
