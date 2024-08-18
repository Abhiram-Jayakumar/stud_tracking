from django.shortcuts import redirect, render

from Administrator.models import ExamResult, Faculty, Payment
from faculty.models import AttendanceUpload, DisciplinaryRecord, Parent
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from decimal import Decimal, InvalidOperation


# Create your views here.
def Parent_home(request):
    parent_id = request.session.get('pid')
    parent_name = None
    
    if parent_id:
        # Assuming you have a Parent model with an id field and a name field
        parent = Parent.objects.get(id=parent_id)
        Parent_name = parent.parent_name
    
    return render(request, 'Parent/Parent_home.html', {'parent_name': Parent_name})


def view_disciplinary_records(request):
    # Assuming the parent is logged in and their ID is stored in the session
    parent_id = request.session.get('pid')
    
    if parent_id:
        parent = Parent.objects.get(id=parent_id)
        student = parent.student
        disciplinary_records = DisciplinaryRecord.objects.filter(student=student)
        
        return render(request, 'Parent/View_disp.html', {
            'student': student,
            'disciplinary_records': disciplinary_records
        })
    else:
        return redirect('Student:Login')  # Redirect 
    




def techer_info(request):
    info=Faculty.objects.all()
    return render(request,'Parent/View_teacher.html',{'info':info})



def view_uploaded_attendance(request):
    uploaded_files = AttendanceUpload.objects.all()
    return render(request, 'parent/view_attendance.html', {'uploaded_files': uploaded_files})



def view_exam_results_by_parent(request):
    # Assuming the parent is logged in and their ID is stored in the session
    parent_id = request.session.get('pid')

    if parent_id:
        parent = Parent.objects.get(id=parent_id)
        student = parent.student
        exam_results = ExamResult.objects.filter(student=student).select_related('semester', 'subject')

        # Group exam results by semester
        results_by_semester = {}
        for result in exam_results:
            semester_name = result.semester.semester_name
            if semester_name not in results_by_semester:
                results_by_semester[semester_name] = []
            results_by_semester[semester_name].append(result)
        
        return render(request, 'Parent/View_result.html', {
            'student': student,
            'results_by_semester': results_by_semester
        })
    else:
        return redirect('Student:Login') 
    


def view_parent_profile(request):
    # Assuming the parent's ID is stored in the session after login
    parent_id = request.session.get('pid')

    if parent_id:
        parent = Parent.objects.get(id=parent_id)
        return render(request, 'Parent/view_parent_profile.html', {'parent': parent})
    else:
        return redirect('Student:Login')
    


def update_password(request):
    parent_id = request.session.get('pid')
    if not parent_id:
        return redirect('Student:Login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        parent = Parent.objects.get(id=parent_id)

        if parent.password == current_password and new_password == confirm_password:
            parent.password = new_password  # Direct assignment; manage hashing elsewhere if needed
            parent.save()
            return redirect('Parent:view_parent_profile')

    return render(request, 'Parent/update_password.html')
    




def update_profile(request):
    parent_id = request.session.get('pid')
    
    if parent_id:
        parent = Parent.objects.get(id=parent_id)
        
        if request.method == 'POST':
            parent.parent_name = request.POST.get('parent_name')
            parent.parent_email = request.POST.get('parent_email')
            parent.address = request.POST.get('address')
            parent.save()
            return redirect('Parent:view_parent_profile')
        
        return render(request, 'Parent/update_profile.html', {'parent': parent})
    else:
        return redirect('Student:Login') 
    


def view_parent_payments(request):
    parent_id = request.session.get('pid')
    
    if parent_id:
        parent = Parent.objects.get(id=parent_id)
        student = parent.student
        payments = Payment.objects.filter(student=student)

        # Calculate balance for each payment
        for payment in payments:
            payment.balance = payment.amount - payment.Paid_amount
        
        return render(request, 'Parent/view_payments.html', {'parent': parent, 'student': student, 'payments': payments})
    else:
        return redirect('Parent:Login')






def make_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    
    if request.method == 'POST':
        Paid_amount_str = request.POST.get('paid_amount')
        
        if Paid_amount_str:
            try:
                Paid_amount = Decimal(Paid_amount_str)
                # Add the new payment amount to the existing Paid_amount
                payment.Paid_amount += Paid_amount
                # Update the status based on the new Paid_amount
                payment.status = 'Paid' if payment.Paid_amount >= payment.amount else 'Partial'
                payment.save()
                
                return redirect('Parent:view_parent_payments')
            except (ValueError, InvalidOperation):
                print("Invalid amount entered")
    
    return render(request, 'Parent/Payment.html', {'payment': payment})