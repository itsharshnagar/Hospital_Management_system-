from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .filters import PatientFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# PatientFilter = OrderFilter

# Create your vie

from django.urls import reverse

def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('dashboard'))
            else:
                messages.error(request, 'Invalid username or password')
                return redirect(reverse('login'))
        else:
            return render(request, 'main/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))




def dashboard(request):
    try:
        patients = Patient.objects.all()
        patient_count = patients.count()
        patients_recovered = Patient.objects.filter(status="Recovered")
        patients_deceased = Patient.objects.filter(status="Deceased")
        deceased_count = patients_deceased.count()
        recovered_count = patients_recovered.count()
        beds = Bed.objects.all()
        beds_available = Bed.objects.filter(occupied=False).count()
        context = {
            'patient_count': patient_count,
            'recovered_count': recovered_count,
            'beds_available': beds_available,
            'deceased_count': deceased_count,
            'beds': beds
        }
        return render(request, 'main/dashboard.html', context)
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {e}")
        return redirect(reverse('login'))

def add_patient(request):
    beds = Bed.objects.filter(occupied=False)
    doctors = Doctor.objects.all()
    if request.method == "POST":
        try:
            name = request.POST['name']
            phone_num = request.POST['phone_num']
            patient_relative_name = request.POST['patient_relative_name']
            patient_relative_contact = request.POST['patient_relative_contact']
            address = request.POST['address']
            symptoms = request.POST['symptoms']
            prior_ailments = request.POST['prior_ailments']
            bed_num_sent = request.POST['bed_num']
            bed_num = Bed.objects.get(bed_number=bed_num_sent)
            dob = request.POST['dob']
            status = request.POST['status']
            doctor_name = request.POST['doctor']
            doctor = Doctor.objects.get(name=doctor_name)
            patient = Patient.objects.create(
                name=name,
                phone_num=phone_num,
                patient_relative_name=patient_relative_name,
                patient_relative_contact=patient_relative_contact,
                address=address,
                symptoms=symptoms,
                prior_ailments=prior_ailments,
                bed_num=bed_num,
                dob=dob,
                doctor=doctor,
                status=status
            )
            patient.save()

            bed = Bed.objects.get(bed_number=bed_num_sent)
            bed.occupied = True
            bed.save()
            id = patient.id
            return redirect(reverse('patient', args=[id]))
        except Bed.DoesNotExist:
            messages.error(request, "Selected bed does not exist.")
        except Doctor.DoesNotExist:
            messages.error(request, "Selected doctor does not exist.")
        except Exception as e:
            messages.error(request, f"Error adding patient: {e}")
        
    context = {
        'beds': beds,
        'doctors': doctors
    }
    return render(request, 'main/add_patient.html', context)

def patient(request, pk):
    try:
        patient = Patient.objects.get(id=pk)
    except Patient.DoesNotExist:
        messages.error(request, "Patient not found.")
        return redirect(reverse('patient_list'))

    if request.method == "POST":
        try:
            doctor_name = request.POST['doctor']
            doctor_time = request.POST['doctor_time']
            doctor_notes = request.POST['doctor_notes']
            mobile = request.POST['mobile']
            mobile2 = request.POST['mobile2']
            relativeName = request.POST['relativeName']
            address = request.POST['location']
            status = request.POST['status']
            doctor = Doctor.objects.get(name=doctor_name)

            patient.phone_num = mobile
            patient.patient_relative_contact = mobile2
            patient.patient_relative_name = relativeName
            patient.address = address
            patient.doctor = doctor
            patient.doctors_visiting_time = doctor_time
            patient.doctors_notes = doctor_notes
            patient.status = status
            patient.save()
        except Doctor.DoesNotExist:
            messages.error(request, "Selected doctor does not exist.")
        except Exception as e:
            messages.error(request, f"Error updating patient: {e}")

    context = {
        'patient': patient
    }
    return render(request, 'main/patient.html', context)


def patient_list(request):
    try:
        patients = Patient.objects.all()

        # filtering
        myFilter = PatientFilter(request.GET, queryset=patients)

        patients = myFilter.qs
        context = {
            'patients': patients,
            'myFilter': myFilter
        }

        return render(request, 'main/patient_list.html', context)
    except Exception as e:
        messages.error(request, f"Error loading patient list: {e}")
        return redirect(reverse('dashboard'))

'''
def autocomplete(request):
    if patient in request.GET:
        name = Patient.objects.filter(name__icontains=request.GET.get(patient))
        name = ['js', 'python']
        
        names = list()
        names.append('Shyren')
        print(names)
        for patient_name in name:
            names.append(patient_name.name)
        return JsonResponse(names, safe=False)
    return render (request, 'main/patient_list.html')
'''

def autosuggest(request):
    query_original = request.GET.get('term')
    queryset = Patient.objects.filter(name__icontains=query_original)
    mylist = [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def autodoctor(request):
    query_original = request.GET.get('term')
    queryset = Doctor.objects.filter(name__icontains=query_original)
    mylist = [x.name for x in queryset]
    return JsonResponse(mylist, safe=False)

def info(request):
    return render(request, "main/info.html")
