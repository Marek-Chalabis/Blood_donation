import pendulum
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, mixins, status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from info.models import Donation, Patient
from users.models import Profile
from .serializers import (
    DonationCustomFilter,
    DonationDetailSerializer,
    DonationSerializer,
    PatientCustomFilter,
    PatientSerializers,
    UserSerializer,
)


@method_decorator(cache_page(60 * 60 * 24), name="dispatch")
class PublicInfoViewSet(viewsets.ViewSet):
    blood_groups = {
        "0 Rh+",
        "A Rh+",
        "B Rh+",
        "AB Rh+",
        "0 Rh-",
        "A Rh-",
        "B Rh-",
        "AB Rh-",
    }
    branches = Profile.objects.values_list("branch", flat=True).distinct()
    lookup_field = "branch"
    permission_classes = [AllowAny]

    def list(self, request):
        blood = self.set_of_bloods()
        percentage_blood_share = self.percentage_of_blood_group(blood)
        state_of_blood_supply = self.blood_state(percentage_blood_share)

        return Response(
            {
                "Branches": self.branches,
                "percentage_blood_share": percentage_blood_share,
                "state_of_blood_supply": state_of_blood_supply,
            }
        )

    def retrieve(self, request, branch=None):
        branch = branch.capitalize()
        if branch in self.branches:
            blood = self.set_of_bloods(branch)
            percentage_blood_share = self.percentage_of_blood_group(blood, branch)
            state_of_blood_supply = self.blood_state(percentage_blood_share)
            return Response(
                {
                    "Branch": branch,
                    "percentage_blood_share": percentage_blood_share,
                    "state_of_blood_supply": state_of_blood_supply,
                }
            )
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={
                    "detail": f"There is no branch: {branch}",
                    "available branches": self.branches,
                },
            )

    def set_of_bloods(self, branch=None):
        """ returns sorted set of (blood_group, number of donations with this blood_group)"""

        if branch is None:
            blood = set(
                Donation.objects.select_related("patient", "medical_staff")
                    .values_list("patient__blood_group")
                    .annotate(
                    total=Count(
                        "id",
                        filter=Q(accept_donate=True, medical_staff__is_staff=False),
                    )
                )
            )
        else:
            blood = set(
                Donation.objects.select_related(
                    "patient", "medical_staff", "medical_staff__profile"
                )
                    .values_list("patient__blood_group")
                    .annotate(
                    total=Count(
                        "id",
                        filter=Q(
                            accept_donate=True,
                            medical_staff__is_staff=False,
                            medical_staff__profile__branch=branch,
                        ),
                    )
                )
            )

        if len(self.blood_groups) != len(blood):
            # checks if there is a blood that don't appear in blood groups and add it to set
            current_list_of_bloods = {blood_type for (blood_type, _) in blood}
            missing_bloods = self.blood_groups.difference(current_list_of_bloods)
            for missing_blood in missing_bloods:
                blood.add((missing_blood, 0))

        return sorted(blood, key=lambda x: x[1], reverse=True)

    def percentage_of_blood_group(self, set_bloods, branch=None):
        """ return dictionary with % of blood group(blood_group: number)"""

        if branch is None:
            current_blood_donations = Donation.objects.filter(
                accept_donate=True
            ).count()
        else:
            current_blood_donations = (
                Donation.objects.select_related("medical_staff__profile")
                    .filter(accept_donate=True, medical_staff__profile__branch=branch)
                    .count()
            )

        return {
            blood_group: round((number_of_donations * 100) / current_blood_donations, 2)
            for (blood_group, number_of_donations) in set_bloods
        }

    def blood_state(self, bloods):
        """ random logic behind blood status"""
        return {
            key: (100 if value * 8 > 100 else value * 8)
            for (key, value) in bloods.items()
        }


class UserPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 500


@method_decorator(cache_page(60 * 60 * 24), name="dispatch")
class UserViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    serializer_class = UserSerializer
    queryset = User.objects.select_related("profile").order_by("id")
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "username",
        "last_name",
        "email",
        "profile__position",
        "profile__branch",
    ]
    pagination_class = UserPagination
    permission_classes = [IsAuthenticated]


class DonationPagination(PageNumberPagination):
    page_size = 250
    page_size_query_param = "page_size"
    max_page_size = 2000


@method_decorator(cache_page(60 * 15), name="dispatch")
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.select_related(
        "medical_staff", "medical_staff__profile", "patient"
    ).order_by("date_of_donation")
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    pagination_class = DonationPagination
    filterset_class = DonationCustomFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DonationDetailSerializer
        return DonationSerializer

    def get_permissions(self):
        if self.action == "destroy" or self.action == "update":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(medical_staff=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = "page_size"
    max_page_size = 1000


@method_decorator(cache_page(60 * 39), name="dispatch")
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializers
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]
    pagination_class = PatientPagination
    filterset_class = PatientCustomFilter

    def get_queryset(self):
        not_able_donation_id = (
            Donation.objects.select_related("patient")
                .filter(
                Q(date_of_donation__gte=pendulum.now().subtract(days=90))
                & Q(accept_donate=True)
            )
                .values_list("patient__id", flat=True)
        )

        queryset = (
            Patient.objects.select_related("registered_by", "registered_by__profile")
                .prefetch_related("donation_set")
                .annotate(
                can_donate=models.Case(
                    models.When(id__in=not_able_donation_id, then=False),
                    default=models.Value(True),
                    output_field=models.BooleanField(),
                )
            )
                .order_by("id")
        )
        return queryset

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = PatientSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(registered_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            patient = self.get_object()
            patient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.ProtectedError as e:
            return Response(
                status=status.HTTP_423_LOCKED,
                data={
                    "Information": "Patient in DB is Protected first "
                                   "you need to delete all donations with him/her",
                    "detail": str(e),
                },
            )
