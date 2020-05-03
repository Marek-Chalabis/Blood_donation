from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import PatientFilter
from .models import Patient, Donation
from django.contrib.auth.models import User
from .forms import PatientForm, DonationForm, InfoForDonor, UpdatePatientForm
from django.db.models import Count, F, Value, Max, Case, When, CharField, ExpressionWrapper, Q
from users.models import Profile
from django.db.models.functions import Concat
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# =========================== VIEWS FOR EVERYONE ============================


def info_main(request):
    available_cities = User.objects.values_list('profile__branch', flat=True).distinct()
    current_blood_status = Donation.objects.filter(accept_donate=True).count()
    current_blood_status_for_blood = current_blood_status / 8
    blood = Patient.objects.values_list('blood_group').filter(donation__accept_donate=True)\
        .annotate(total=Count('donation')).order_by('total')

    context = {
        # just to add some logic into view
        'blood_all': {blood_tuple[0]: round((blood_tuple[1] * 100) / current_blood_status, 2) for blood_tuple in blood},
        'bloods':  {blood_tuple[0]: round((blood_tuple[1] * 100) / current_blood_status_for_blood, 2)
                    for blood_tuple in blood},
        'cities': available_cities
    }
    return render(request, 'main_info.html', context)


def info_branch(request, branch):
    context = {'branch': branch}
    # remove actual branch from cities
    available_cities = list(User.objects.values_list('profile__branch', flat=True).distinct())
    available_cities.remove(branch)

    current_blood_status = Donation.objects.filter(
        accept_donate=True, medical_staff__profile__branch=branch, medical_staff__is_staff=False).count()

    current_blood_status_for_blood = current_blood_status / 8

    blood = Patient.objects.values_list('blood_group').filter(
        donation__accept_donate=True, medical_staff__profile__branch=branch, medical_staff__is_staff=False)\
        .annotate(total=Count('donation')).order_by('total')

    staff = Profile.objects.filter(branch=branch, user__is_staff=False).select_related('user').all()

    # just to add some logic into view
    context['blood_all'] = {blood_tuple[0]: round((blood_tuple[1] * 100)
                                                  / current_blood_status, 2) for blood_tuple in blood}
    context['bloods'] = {blood_tuple[0]: round((blood_tuple[1] * 100)
                                               / current_blood_status_for_blood, 2) for blood_tuple in blood}
    context['cities'] = available_cities
    context['staff'] = staff

    return render(request, 'branch_info.html', context)


def info_donor(request):
    context = {}
    if request.method == 'POST':
        form = InfoForDonor(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            donor_check = Patient.objects.filter(pesel=pesel)
            # checks if donor was in db
            if donor_check.exists():
                donor = donor_check[0]
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                # checks if data is correct
                if first_name != donor.first_name:
                    messages.warning(request, f'Fist name({first_name}) is not valid for-{pesel}')
                elif last_name != donor.last_name:
                    messages.warning(request, f'Last name({last_name}) is not valid for-{pesel}')
                else:
                    given_blood_litres = Patient.given_blood_litres(donor)
                    context['donor'] = donor
                    context['given_blood_litres'] = given_blood_litres
                    context['status'] = Patient.donor_status(donor, given_blood_litres)
                    context['can_donate'] = Patient.can_donate(donor)
                    context['form'] = form
                    return render(request, 'donor_info.html', context)
            else:
                messages.warning(request, f'{pesel} - Does Not exists in database')
    else:
        form = InfoForDonor()
    context['form'] = form
    return render(request, 'donor_info.html', context)


# =================== REQUIRE LOGIN =============

@login_required
def donate(request):
    if request.method == "POST":
        pesel = request.POST.get("pesel")
        donor = Patient.objects.filter(pesel=pesel)
        # checks if donor was in db
        if donor.exists():
            return redirect('blood-donation', donor_id=donor[0].id)
        else:
            messages.warning(request, f'{pesel} - Does Not exists in database, register him/her')
    return render(request, 'donate.html')


@login_required
def blood_donation(request, donor_id):
    donor = Patient.objects.get(id=donor_id)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.instance.medical_staff = request.user
            form.instance.patient = donor
            form.save()
            return redirect('donate')
    else:
        form = DonationForm()
    context = {
        'form': form,
        'donor': donor,
    }
    return render(request, 'blood_donation.html', context)


@method_decorator(login_required, name='dispatch')
@method_decorator(cache_page(60 * 60), name='dispatch')
class PatientListView(ListView): #LoginRequiredMixin
    # adds dates of last correct donation
    queryset = Patient.objects\
        .annotate(last_correct_donation=Max('donation__date_of_donation', filter=Q(donation__accept_donate=True)))
    template_name = 'Patient/patient.html'
    ordering = ['last_name', 'first_name']
    context_object_name = 'patients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET, queryset=self.get_queryset())
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(cache_page(60 * 15), name='dispatch')
class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'Patient/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donor = context['object']
        given_blood_litres = Patient.given_blood_litres(donor)
        context['donor'] = donor
        context['given_blood_litres'] = given_blood_litres
        context['status'] = Patient.donor_status(donor, given_blood_litres)
        context['can_donate'] = Patient.can_donate(donor)
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    template_name = 'Patient/patient_form.html'
    form_class = PatientForm
    success_message = "Donor was registered successfully"

    def form_valid(self, form):
        form.instance.medical_staff = self.request.user
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Patient
    template_name = 'Patient/patient_update_form.html'
    form_class = UpdatePatientForm
    success_message = "Donor was updated successfully"
    template_name_suffix = '_update_form'
