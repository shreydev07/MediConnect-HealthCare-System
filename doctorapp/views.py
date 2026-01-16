from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.mail import send_mail
from doctorapp.models import *
from mainapp.models import Appointment
from adminapp.models import Notification

# Helper function to check if doctor is logged in
def is_doctor_logged_in(request):
    return 'doctor_id' in request.session

@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctorhome(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    return render(request, 'doctorhome.html')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def vpa(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    appointments = Appointment.objects.all().order_by('appointment_date', 'appointment_time')
    return render(request, 'vpa.html', {'appointments': appointments})


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def markaproove(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=id)
    # move appointment to processing (doctor approved/rescheduled moves to processing)
    appointment.status = Appointment.STATUS_PROCESSING
    appointment.save()

    # Email content
    subject = 'Appointment Confirmation'
    message = f"""
Dear {appointment.name},

Your appointment with Dr. {appointment.doctor.doctor_name} ({appointment.doctor_speciality}) 
has been approved for {appointment.appointment_date} at {appointment.appointment_time}.
Thank you for choosing MediConnect!
"""
    recipient = appointment.email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='mediconnect7781@gmail.com',
            recipient_list=[recipient],
            fail_silently=False,
        )
        messages.success(request, f"Appointment approved and email sent to {recipient}.")
    except Exception as e:
        messages.warning(request, "Appointment approved, but email failed to send.")

    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def rejectappointment(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=id)
    # Only allow moving forward from pending -> rejected
    if appointment.status == Appointment.STATUS_PENDING:
        appointment.status = Appointment.STATUS_REJECTED
        appointment.save()

        subject = 'Appointment Rejected'
        message = f"Dear {appointment.name},\n\nWe are sorry to inform you that your appointment with Dr. {appointment.doctor.doctor_name} on {appointment.appointment_date} at {appointment.appointment_time} has been rejected. Please try again later or contact the clinic for alternatives.\n\nRegards,\nMediConnect"
        try:
            send_mail(subject=subject, message=message, from_email='mediconnect7781@gmail.com', recipient_list=[appointment.email], fail_silently=False)
            messages.info(request, f"Rejection email sent to {appointment.email}.")
        except Exception:
            messages.warning(request, "Appointment rejected, but failed to send email.")

    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def rescheduleappointment(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=id)
    # Only allow moving forward from pending -> processing
    if appointment.status == Appointment.STATUS_PENDING:
        appointment.status = Appointment.STATUS_PROCESSING
        appointment.save()

        subject = 'Appointment Rescheduled/Processing'
        message = f"Dear {appointment.name},\n\nYour appointment with Dr. {appointment.doctor.doctor_name} on {appointment.appointment_date} at {appointment.appointment_time} has been moved to processing for rescheduling. The clinic will contact you with a new slot.\n\nRegards,\nMediConnect"
        try:
            send_mail(subject=subject, message=message, from_email='mediconnect7781@gmail.com', recipient_list=[appointment.email], fail_silently=False)
            messages.info(request, f"Reschedule email sent to {appointment.email}.")
        except Exception:
            messages.warning(request, "Appointment marked for reschedule, but failed to send email.")

    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def completeappointment(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')

    appointment = get_object_or_404(Appointment, id=id)
    # Only allow completing from processing -> completed
    if appointment.status == Appointment.STATUS_PROCESSING:
        appointment.status = Appointment.STATUS_COMPLETED
        appointment.is_completed = True
        appointment.save()
        messages.success(request, f"Appointment (id={id}) marked completed.")

    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def deleteappointment(request, id):
    if not is_doctor_logged_in(request):
        return redirect('login')
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('doctorapp:vpa')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def doctorlogout(request):
    request.session.flush()
    return redirect('login')


@cache_control(no_store=True, no_cache=True, must_revalidate=True)
def viewnotifications(request):
    if not is_doctor_logged_in(request):
        return redirect('login')
    notifications = Notification.objects.all().order_by('created_at')
    # template files are located in doctorapp/templates/, so reference the file directly
    return render(request, 'viewnotifications.html', {'notifications': notifications})
