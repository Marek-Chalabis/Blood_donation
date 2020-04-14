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


# =========================== VIEWS FOR EVERYONE ============================
def info_main(request):
    blood_all = {}
    current_blood_status = Donation.objects.filter(accept_donate=True).count()
    current_blood_status_for_blood = Donation.objects.count() / 8
    for blood in Patient.objects.values('blood_group'):
        """
        counts all donated blood for specific type
        """
        blood_all[blood['blood_group']] = Donation.objects.filter(patient__blood_group=blood['blood_group'],
                                                                  accept_donate=True).count()
    # sorts from highest to lowest
    blood_all = {k: v for k, v in sorted(blood_all.items(), key=lambda item: item[1])}
    context = {
        'blood_all': {k: round((v * 100) / current_blood_status, 2) for k, v in blood_all.items()},
        'bloods': {k: round((v * 100) / current_blood_status_for_blood, 2) for k, v in blood_all.items()},
    }
    return render(request, 'main_info.html', context)


def info_branch(request, branch):
    blood_all = {}
    current_blood_status = Donation.objects.filter(accept_donate=True, medical_staff__profile__branch=branch,
                                                   medical_staff__is_staff=False).count()
    current_blood_status_for_blood = Donation.objects.filter(medical_staff__profile__branch=branch,
                                                             medical_staff__is_staff=False).count() / 8
    for blood in Patient.objects.values('blood_group'):
        blood_all[blood['blood_group']] = Donation.objects.filter(patient__blood_group=blood['blood_group'],
                                                                  accept_donate=True,
                                                                  medical_staff__profile__branch=branch,
                                                                  medical_staff__is_staff=False
                                                                  ).count()
    blood_all = {k: v for k, v in sorted(blood_all.items(), key=lambda item: item[1])}
    context = {
        'blood_all': {k: round((v * 100) / current_blood_status, 2) for k, v in blood_all.items()},
        'bloods': {k: round((v * 100) / current_blood_status_for_blood, 2) for k, v in blood_all.items()},
        'branch': branch,
        'staff': User.objects.filter(profile__branch=branch, is_staff=False).all()
    }
    return render(request, 'branch_info.html', context)


def info_donor(request):
    context = {
        'percentage_admitted': round(
            (Donation.objects.filter(accept_donate=True).count() / Donation.objects.count()) * 100, 2),
    }
    if request.method == 'POST':
        form = InfoForDonor(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            if Patient.objects.filter(pesel=pesel).exists():
                donor = Patient.objects.get(pesel=pesel)
                last_name = form.cleaned_data['last_name']
                first_name = form.cleaned_data['first_name']
                if first_name != donor.first_name:
                    messages.warning(request, f'{first_name} is not valid for-{pesel}')
                elif last_name != donor.last_name:
                    messages.warning(request, f'{last_name} is not valid for-{pesel}')
                else:
                    context['donor'] = donor
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
        if Patient.objects.filter(pesel=pesel).exists():
            donor = Patient.objects.get(pesel=pesel)
            return redirect('blood-donation', donor_id=donor.id)
        else:
            messages.warning(request, f'{pesel} - Does Not exists in database, register him/her')
    return render(request, 'donate.html', {'donors': Patient.objects.count()})


@login_required
def blood_donation(request, donor_id):
    patient = Patient.objects.get(id=donor_id)
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.instance.medical_staff = request.user
            form.instance.patient = Patient.objects.get(id=donor_id)
            form.save()
            return redirect('donate')
    else:
        form = DonationForm()
    context = {
        'form': form,
        'patient': patient,
        'history': Donation.objects.filter(patient=patient).order_by('-date_of_donation').all()
    }
    return render(request, 'blood_donation.html', context)


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'Patient/patient.html'
    ordering = ['last_name', 'first_name']
    context_object_name = 'patients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PatientFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'Patient/patient_detail.html'


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
