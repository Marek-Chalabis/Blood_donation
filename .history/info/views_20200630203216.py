from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Max, Q
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from users.models import Profile
from .filters import PatientFilter
from .forms import PatientForm, DonationForm, InfoForDonor, UpdatePatientForm
from .models import Patient, Donation


# =========================== VIEWS FOR EVERYONE ============================


class BloodInformation:
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

    @staticmethod
    def set_of_bloods(branch=None):
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

        # checks if there is a blood that don't appear in blood groups
        if len(BloodInformation.blood_groups) != len(blood):
            # checks what type of blood is missing
            current_list_of_bloods = {blood_type for (blood_type, _) in blood}
            missing_bloods = BloodInformation.blood_groups.difference(
                current_list_of_bloods
            )
            # adds it to base set
            for missing_blood in missing_bloods:
                blood.add((missing_blood, 0))

        return sorted(blood, key=lambda x: x[1])

    @staticmethod
    def percentage_of_blood_group(set_bloods, branch=None):
        """ return dictionary with % of blood group(blood_group: number)"""

        # number of correct donations
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

    @staticmethod
    def blood_state(bloods):
        """ random logic behind blood status"""
        return {
            key: (100 if value * 8 > 100 else value * 8)
            for (key, value) in bloods.items()
        }


def info_main(request):
    blood = BloodInformation.set_of_bloods()
    percentage_blood_share = BloodInformation.percentage_of_blood_group(blood)
    state_of_blood_supply = BloodInformation.blood_state(percentage_blood_share)

    context = {
        # just to add some logic into view
        "blood_all": percentage_blood_share,
        "bloods": state_of_blood_supply,
        "cities": BloodInformation.branches,
    }
    return render(request, "main_info.html", context)


def info_branch(request, branch):
    blood = BloodInformation.set_of_bloods(branch)
    percentage_blood_share = BloodInformation.percentage_of_blood_group(blood, branch)
    state_of_blood_supply = BloodInformation.blood_state(percentage_blood_share)

    available_cities = list(BloodInformation.branches)
    available_cities.remove(branch)

    staff = (
        Profile.objects.select_related("user")
        .filter(branch=branch, user__is_staff=False)
        .all()
    )

    context = {
        "branch": branch,
        "blood_all": percentage_blood_share,
        "bloods": state_of_blood_supply,
        "cities": available_cities,
        "staff": staff,
    }
    return render(request, "branch_info.html", context)


def info_donor(request):
    context = {}
    if request.method == "POST":
        form = InfoForDonor(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data["pesel"]
            donor_check = Patient.objects.filter(pesel=pesel)
            # checks if donor was in db
            if donor_check.exists():
                donor = donor_check[0]
                last_name = form.cleaned_data["last_name"]
                first_name = form.cleaned_data["first_name"]
                # checks if data is correct
                if first_name != donor.first_name:
                    messages.warning(
                        request, f"Fist name({first_name}) is not valid for-{pesel}"
                    )
                elif last_name != donor.last_name:
                    messages.warning(
                        request, f"Last name({last_name}) is not valid for-{pesel}"
                    )
                else:
                    given_blood_litres = Patient.given_blood_litres(donor)
                    context["donor"] = donor
                    context["given_blood_litres"] = given_blood_litres
                    context["status"] = Patient.donor_status(donor, given_blood_litres)
                    context["can_donate"] = Patient.can_donate(donor)
                    context["form"] = form
                    return render(request, "donor_info.html", context)
            else:
                messages.warning(request, f"{pesel} - Does Not exists in database")
    else:
        form = InfoForDonor()
    context["form"] = form
    return render(request, "donor_info.html", context)


# ======================== REQUIRE LOGIN ==========================


@login_required
def donate(request):
    if request.method == "POST":
        pesel = request.POST.get("pesel")
        donor = Patient.objects.filter(pesel=pesel)
        # checks if donor was in db
        if donor.exists():
            return redirect("blood-donation", donor_id=donor[0].id)
        else:
            messages.warning(
                request, f"{pesel} - Does Not exists in database, register him/her"
            )
    return render(request, "donate.html")


@login_required
def blood_donation(request, donor_id):
    donor = Patient.objects.get(id=donor_id)
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            form.instance.medical_staff = request.user
            form.instance.patient = donor
            form.save()
            return redirect("donate")
    else:
        form = DonationForm()
    context = {"form": form, "donor": donor}
    return render(request, "blood_donation.html", context)


@method_decorator(login_required, name="dispatch")
@method_decorator(cache_page(60 * 60), name="dispatch")
class PatientListView(ListView):
    # adds dates of last correct donation
    queryset = Patient.objects.annotate(
        last_correct_donation=Max(
            "donation__date_of_donation", filter=Q(donation__accept_donate=True)
        )
    )
    template_name = "Patient/patient.html"
    ordering = ["last_name", "first_name"]
    context_object_name = "patients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PatientFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


@method_decorator(login_required, name="dispatch")
@method_decorator(cache_page(60 * 15), name="dispatch")
class PatientDetailView(DetailView):
    model = Patient
    template_name = "Patient/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donor = context["object"]
        given_blood_litres = Patient.given_blood_litres(donor)
        context["donor"] = donor
        context["given_blood_litres"] = given_blood_litres
        context["status"] = Patient.donor_status(donor, given_blood_litres)
        context["can_donate"] = Patient.can_donate(donor)
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = "Patient/patient_form.html"
    form_class = PatientForm
    success_message = "Donor was registered successfully"

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patient
    template_name = "Patient/patient_update_form.html"
    form_class = UpdatePatientForm
    success_message = "Donor was updated successfully"
    template_name_suffix = "_update_form"

