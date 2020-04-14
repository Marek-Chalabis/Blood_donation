import django_filters
from .models import Patient, Donation
import datetime


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
        today = datetime.datetime.today()
        today = datetime.date(today.year, today.month, today.day)
        accept_date = today - datetime.timedelta(days=90)
        able_to_donate = []
        for q in queryset:
            if Donation.objects.filter(patient=q).exists():
                if q.donation_set.last().date_of_donation < accept_date:
                    able_to_donate.append(q.id)
        if value == 'Yes':
            return queryset.filter(id__in=able_to_donate)
        elif value == 'No':
            not_able_to_donate = set(list(q.id for q in queryset)).difference(able_to_donate)
            return queryset.filter(id__in=not_able_to_donate)
