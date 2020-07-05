import pytest
from django.urls import reverse, resolve


@pytest.mark.parametrize(
    "name, kwargs",
    [
        ('main', None),
        ('info-branch', {'branch': 'test_BRANCH'}),
        ('info-donor', None),
        ('donate', None),
        ('blood-donation', {'donor_id': 1}),
        ('patient-home', None),
        ('patient-detail', {'pk': 1}),
        ('patient-create', None),
        ('patient-update', {'pk': 1}),
    ],
)
def test_urls(name, kwargs):
    path = reverse(name, kwargs=kwargs)
    assert resolve(path).view_name == name
