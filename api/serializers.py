import django_filters
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from info.models import Donation, Patient
from localflavor.pl.forms import PLPESELField
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

# ========USERS========


class UserSerializer(FlexFieldsModelSerializer):
    image = serializers.ImageField(source="profile.image", read_only=True, use_url=True)
    position = serializers.CharField(source="profile.position", read_only=True)
    branch = serializers.CharField(source="profile.branch", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "branch",
            "image",
        ]


# ========DONATIONS========


class DonationCustomFilter(django_filters.FilterSet):
    patient = django_filters.BaseInFilter(method="search_in")
    medical_staff = django_filters.BaseInFilter(method="search_in")

    class Meta:
        model = Donation
        fields = {
            "id": ["in"],
            "date_of_donation": [
                "exact",
                "icontains",
                "gt",
                "gte",
                "lt",
                "lte",
                "year",
                "month",
                "day",
            ],
            "accept_donate": ["exact"],
            "refuse_information": ["icontains"],
        }

    def search_in(self, queryset, name, value):
        if name == "medical_staff":
            return queryset.filter(medical_staff_id__in=value)
        elif name == "patient":
            return queryset.filter(patient_id__in=value)


class DonationSerializer(FlexFieldsModelSerializer):
    medical_staff = serializers.PrimaryKeyRelatedField(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    blood_group = serializers.CharField(source="patient.blood_group", read_only=True)

    class Meta:
        model = Donation
        fields = [
            "medical_staff",
            "patient",
            "blood_group",
            "date_of_donation",
            "accept_donate",
            "refuse_information",
        ]
        read_only_fields = ["date_of_donation"]

    def validate(self, data):
        # if donation is refuse user should return information why
        if data["accept_donate"] is False:
            if "refuse_information" not in data:
                raise ValidationError("If you refuse donation, write why")
            elif data["refuse_information"] is None or data["refuse_information"] == "":
                raise ValidationError("Refuse information needs to be provided")
        return data


class PatientShortInfoSerializers(FlexFieldsModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "blood_group",
            "phone_number",
            "registered_by",
        ]


class DonationDetailSerializer(FlexFieldsModelSerializer):
    medical_staff = UserSerializer(read_only=True)
    patient = PatientShortInfoSerializers(read_only=True)

    class Meta:
        model = Donation
        fields = [
            "medical_staff",
            "patient",
            "date_of_donation",
            "accept_donate",
            "refuse_information",
        ]


# ========PATIENTS========


class PatientCustomFilter(django_filters.FilterSet):
    can_donate = django_filters.BooleanFilter(field_name="can_donate")
    search = django_filters.CharFilter(method="full_search")
    registered_by = django_filters.BaseInFilter(method="search_in")

    class Meta:
        model = Patient
        fields = {
            "id": ["in"],
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
            "pesel": ["exact", "icontains"],
            "blood_group": ["exact", "icontains"],
            "gender": ["exact"],
            "email": ["exact", "icontains"],
            "phone_number": ["exact", "icontains"],
            "date_of_register": [
                "exact",
                "icontains",
                "gt",
                "gte",
                "lt",
                "lte",
                "year",
                "month",
                "day",
            ]
        }

    def full_search(self, queryset, name, value):
        # full search in given fields
        return queryset.filter(
            Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
            | Q(pesel__icontains=value)
            | Q(email__icontains=value)
            | Q(phone_number__icontains=value)
        )

    def search_in(self, queryset, name, value):
        return queryset.filter(registered_by_id__in=value)


class DonationForPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = [
            "id",
            "date_of_donation",
            "accept_donate",
            "refuse_information",
            "medical_staff",
        ]


class PatientSerializers(FlexFieldsModelSerializer):
    can_donate = serializers.SerializerMethodField()
    registered_by = UserSerializer(read_only=True)
    donation_set = DonationForPatientSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = (
            [
                "id",
                "first_name",
                "last_name",
                "pesel",
                "blood_group",
                "gender",
                "email",
                "phone_number",
                "date_of_register",
                "registered_by",
            ]
            + ["can_donate"]
            + ["donation_set"]
        )
        read_only_fields = ["date_of_register"]

    def validate(self, data):
        pesel_check = PLPESELField()
        pesel_check.clean(data["pesel"])
        return data

    def get_can_donate(self, object):
        try:
            self._kwargs["context"]
            return object.can_donate
        except KeyError:
            # if object was just created there will be no 'context' so always ready to donate
            return True
