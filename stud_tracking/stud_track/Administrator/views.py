from django.shortcuts import redirect, render

from Administrator.models import Faculty, Payment
from faculty.models import Semester, Student

# Create your views here.
def index(request):
    return render(request,'Administrator/index.html')


def Admin_home(request):
    return render(request,'Administrator/Admin_home.html')



def register_faculty(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        password = request.POST.get('password')

        faculty = Faculty(name=name, dob=dob, email=email, phone=phone, gender=gender, department=department, qualification=qualification, experience=experience,password=password)
        faculty.save()

        return redirect('Administrator:Admin_home')

    return render(request, 'Administrator/Reg_faculty.html')


def view_student_details(request):
    students = Student.objects.all()
    return render(request, 'Administrator/view_student_details.html', {'students': students})



def add_payment(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        semester_id = request.POST.get('sem')
        amount = request.POST.get('amount')
        payment_due_date = request.POST.get('payment_due_date')
        
        if student_id and semester_id and amount and payment_due_date:
            student = Student.objects.get(id=student_id)
            semester = Semester.objects.get(id=semester_id)
            Payment.objects.create(
                student=student,
                sem=semester,
                amount=amount,
                payment_due_date=payment_due_date
            )
            return redirect('Administrator:Admin_home')
    
    students = Student.objects.all()
    semesters = Semester.objects.all()
    return render(request, 'Administrator/add_payment.html', {'students': students, 'semesters': semesters})




def view_student_payments(request):
    # Fetch all payments. You might want to add filters or order by specific fields.
    payments = Payment.objects.select_related('student', 'sem').all()
    for payment in payments:
            payment.balance = payment.amount - payment.Paid_amount

    return render(request, 'Administrator/view_student_payments.html', {'payments': payments})
