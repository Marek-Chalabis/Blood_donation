import django_filters
from .models import Patient, Donation
import datetime
from django.db.models import Q


class PatientFilter(django_filters.FilterSet):
    BLOOD_CHOICES = (('Yes', 'Yes'), ('No', 'No'))
    last_name = django_filters.CharFilter(label='Last Name', lookup_expr='icontains')
    pesel = django_filters.NumberFilter(label='PESEL', lookup_expr='icontains')
    can_donated = django_filters.ChoiceFilter(label='Able to donate', method='can_donate', choices=BLOOD_CHOICES)

    class Meta:
        model = Patient
        fields = ['last_name', 'pesel', 'blood_group', 'can_donated']

    def can_donate(self, queryset, name, value):
        """
        Returns donors that last donate was more then 90 days ago
        """
        # list of id patients  who donated under 90 days from today AND donation was accepted
        not_able_donation_id = Donation.objects.filter(
            Q(date_of_donation__gte=datetime.datetime.now() - datetime.timedelta(days=90)) &
            Q(accept_donate=True)) \
            .all().values_list('patient__id', flat=True)

        if value == 'Yes':
            return queryset.exclude(id__in=not_able_donation_id)
        elif value == 'No':
            return queryset.filter(id__in=not_able_donation_id)
