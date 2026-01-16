from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mainapp.models import *
from django.core.mail import send_mail

# Admin login required check
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adminhome(req):
    if 'adminid' not in req.session:
        return redirect('login')
    return render(req, 'adminhome.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adminlogout(req):
    req.session.flush()
    return redirect('login')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewstaffrequest(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    stf = StaffRequest.objects.all()
    return render(req, 'viewstaffrequest.html', {'stf': stf})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewstaff(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    staff = StaffRegister.objects.all().order_by('-created_at')
    return render(req, 'viewstaff.html', {'staff': staff})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletestaff(req, id):
    if not req.session.get('adminid'):
        return redirect('login')  # or your custom login page
    staff = get_object_or_404(StaffRegister, id=id)
    staff.delete()
    return redirect('adminapp:viewstaff')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def acceptstaffrequest(req, id):
    if 'adminid' not in req.session:
        return redirect('login')

    # Fetch the request
    staff_req = get_object_or_404(StaffRequest, id=id)

    # Save to StaffRegister
    staff = StaffRegister.objects.create(
        staff_name=staff_req.staff_name,
        staff_email=staff_req.staff_email,
        staff_password=staff_req.staff_password,
        staff_phone=staff_req.staff_phone,
        staff_address=staff_req.staff_address,
    )

    # Prepare email content
    subject = 'Staff Registration Approved'
    message = f"""
    Dear {staff.staff_name},

    Your staff registration at MediConnect has been successfully approved.

    You can now log in and begin using our system with the email you registered.

    Thank you for joining MediConnect!
    """
    recipient = staff.staff_email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='mediconnect7781@gmail.com',  # Your Gmail address
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(req, f"Staff approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(req, "Staff approved, but email could not be sent. Please check your email settings.")

    # Delete the request after approval
    staff_req.delete()
    return redirect('adminapp:viewstaffrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletestaffrequest(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    StaffRequest.objects.filter(id=id).delete()
    return redirect('adminapp:viewstaffrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def addstaff(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    if req.method == 'POST':
        staff_name = req.POST.get('staff_name')
        staff_email = req.POST.get('staff_email')
        staff_password = req.POST.get('staff_password')
        staff_phone = req.POST.get('staff_phone')
        staff_address = req.POST.get('staff_address')

        staff = StaffRegister(
            staff_name=staff_name,
            staff_email=staff_email,
            staff_password=staff_password,
            staff_phone=staff_phone,
            staff_address=staff_address
        )
        staff.save()
        
        return redirect('adminapp:viewstaff')

    prefill = req.GET
    return render(req, 'addstaff.html', {'prefill': prefill})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewdoctorrequest(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    dct = DoctorRequest.objects.all()
    return render(req, 'viewdoctorrequest.html', {'dct': dct})



@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def adddoctor(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    specialities = [
        'General Physician',
        'Obstetrician/Gynecologist (OB/GYN)',
        'Pediatrician',
        'Cardiologist',
        'Orthopaedics'
    ]

    if req.method == 'POST':
        doctor_id = req.POST.get('doctor_id')
        doctor_name = req.POST.get('doctor_name')
        doctors_speciality = req.POST.get('doctors_speciality')
        doctor_email = req.POST.get('doctor_email')
        doctor_password = req.POST.get('doctor_password')
        doctor_phone = req.POST.get('doctor_phone')

        # Create approved doctor entry
        DoctorRegister.objects.create(
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            doctors_speciality=doctors_speciality,
            doctor_email=doctor_email,
            doctor_phone=doctor_phone,
            doctor_password=doctor_password
        )

        return redirect('adminapp:viewdoctor')

    prefill = req.GET
    return render(req, 'adddoctor.html', {
        'prefill': prefill,
        'specialities': specialities
    })


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def acceptdoctorrequest(req, id):
    if 'adminid' not in req.session:
        return redirect('login')

    # Fetch the doctor request
    doc_req = get_object_or_404(DoctorRequest, id=id)

    # Save to DoctorRegister
    doctor = DoctorRegister.objects.create(
        doctor_id=doc_req.doctor_id,
        doctor_name=doc_req.doctor_name,
        doctors_speciality=doc_req.doctors_speciality,
        doctor_email=doc_req.doctor_email,
        doctor_phone=doc_req.doctor_phone,
        doctor_password=doc_req.doctor_password
    )

    # Prepare email content
    subject = 'Doctor Registration Approved'
    message = f"""
    Dear Dr. {doctor.doctor_name},

    Your registration as a {doctor.doctors_speciality} at MediConnect has been successfully approved.

    You can now log in and begin managing your appointments using the email you registered with.

    Thank you for being a part of MediConnect!
    """
    recipient = doctor.doctor_email

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='mediconnect7781@gmail.com',  # Replace with your verified Gmail
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(req, f"Doctor approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(req, "Doctor approved, but email could not be sent. Please check your email settings.")

    # Delete request after processing
    doc_req.delete()
    return redirect('adminapp:viewdoctorrequest')


def deletedoctorrequest(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    DoctorRequest.objects.filter(id=id).delete()
    return redirect('adminapp:viewdoctorrequest')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewdoctor(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    doctors = DoctorRegister.objects.all().order_by('created_at')
    return render(req, 'viewdoctor.html', {'doctors': doctors})

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def dkp(req, doctor_id):
    if not req.session.get('adminid'):
        return redirect('login')  # custom admin login page

    doctor = get_object_or_404(DoctorRegister, doctor_id=doctor_id)
    doctor.delete()
    return redirect('adminapp:viewdoctor')

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewcomplaints(req):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    complaints = Complaints.objects.all().order_by('registered_date')
    return render(req, 'viewcomplaints.html', {'complaints': complaints})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletecomplaint(req, id):
    if 'adminid' not in req.session:  # Ensure admin is logged in
        return redirect('login')
    complaint = get_object_or_404(Complaints, id=id)
    complaint.delete()
    return redirect('adminapp:viewcomplaints')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def addnotification(request):
    if 'adminid' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        message = request.POST.get('message')
        send_to_list = request.POST.getlist('send_to')  # Multiple checkboxes

        if not message or not send_to_list:
            messages.error(request, "Please fill in the message and select at least one recipient.")
            return redirect('adminapp:addnotification')

        for recipient in send_to_list:
            Notification.objects.create(
                message=message,
                send_to=recipient
            )
        messages.success(request, "Notification(s) sent successfully.")
        return redirect('adminapp:viewnotifi')

    return render(request, 'addnotification.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewnotifi(request):
    if 'adminid' not in request.session:
        return redirect('login')
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'viewnotifi.html', {'notifications': notifications})
@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deletenotification(request, id):
    if 'adminid' not in request.session:
        return redirect('login')
    Notification.objects.filter(id=id).delete()
    return redirect('adminapp:viewnotifi')