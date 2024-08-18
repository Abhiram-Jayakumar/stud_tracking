from django.shortcuts import redirect, render

from Administrator.models import Admintable, ExamResult, Faculty, Payment
from Student.models import LeaveApplication
from faculty.models import AttendanceUpload, DisciplinaryRecord, Parent, Student

# Create your views here.
def Student_home(request):
    student_id = request.session.get('sid')
    student_name = None
    
    if student_id:
        # Assuming you have a Student model with an id field and a name field
        student = Student.objects.get(id=student_id)
        student_name = student.name
    
    return render(request, 'Student/Stud_home.html', {'student_name': student_name,'student_id':student_id})


def Login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        flogin=Faculty.objects.filter(email=email,password=password).count()
        Plogin=Parent.objects.filter(parent_email=email,password=password).count()
        Alogin=Admintable.objects.filter(email=email,password=password).count()
        slogin=Student.objects.filter(email=email,password=password).count()


        if flogin > 0:
            fadmin=Faculty.objects.get(email=email,password=password)
            request.session['fid']=fadmin.id
            return redirect('faculty:faculty_home')
        elif Plogin > 0:
            padmin=Parent.objects.get(parent_email=email,password=password)
            request.session['pid']=padmin.id
            return redirect('Parent:Parent_home')
        elif Alogin > 0:
            aadmin=Admintable.objects.get(email=email,password=password)
            request.session['aid']=aadmin.id
            return redirect('Administrator:Admin_home')
        elif slogin > 0:
            sadmin=Student.objects.get(email=email,password=password)
            request.session['sid']=sadmin.id
            return redirect('Student:Student_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"Student/Login.html",{'ERR':error})
    else:
        return render(request, "Student/Login.html")
    



def view_exam_results(request):
    # Assuming the student is logged in and their ID is stored in the session
    student_id = request.session.get('sid')
    
    if student_id:
        student = Student.objects.get(id=student_id)
        exam_results = ExamResult.objects.filter(student=student).select_related('semester', 'subject')

        # Group exam results by semester
        results_by_semester = {}
        for result in exam_results:
            semester_name = result.semester.semester_name
            if semester_name not in results_by_semester:
                results_by_semester[semester_name] = []
            results_by_semester[semester_name].append(result)
        
        return render(request, 'Student/View_result.html', {
            'student': student,
            'results_by_semester': results_by_semester
        })
    else:
        return redirect('Student:Login')  # Redirect to login if no student is logged in




def student_profile(request, student_id):
    student = Student.objects.get(id=student_id)
    return render(request, 'Student/Profile.html', {'student': student})




def apply_leave(request):
    if request.method == 'POST':
        student_id = request.session.get('sid')  # Get student ID from session
        teacher_id = request.POST.get('teacher_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')

        if student_id:
            student = Student.objects.get(id=student_id)
            teacher = Faculty.objects.get(id=teacher_id)

            LeaveApplication.objects.create(
                student=student,
                teacher=teacher,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )

            return redirect('Student:Student_home')  # Redirect to the student's home page after submission

    teachers = Faculty.objects.all()
    return render(request, 'Student/Leave_form.html', {'teachers': teachers})


def view_applied_leaves(request):
    student_id = request.session.get('sid')  # Get student ID from session

    if student_id:
        applied_leaves = LeaveApplication.objects.filter(student__id=student_id)
        return render(request, 'Student/View_applied_leaves.html', {'applied_leaves': applied_leaves})
    
    return redirect('Student:Login')



def view_uploaded_attendance(request):
    uploaded_files = AttendanceUpload.objects.all()
    return render(request, 'Student/view_attendance.html', {'uploaded_files': uploaded_files})




def view_disciplinary_records(request):
    # Assuming the student is logged in and their ID is stored in the session
    student_id = request.session.get('sid')

    if student_id:
        student = Student.objects.get(id=student_id)
        disciplinary_records = DisciplinaryRecord.objects.filter(student=student)
        
        return render(request, 'Student/View_disp.html', {
            'student': student,
            'disciplinary_records': disciplinary_records
        })
    else:
        return redirect('Student:Login')  # Redirect to login if student ID is not found in session




def edit_student_details(request):
    # Assuming the student is logged in and their ID is stored in the session
    student_id = request.session.get('sid')
    
    if student_id:
        student = Student.objects.get(id=student_id)
        
        if request.method == 'POST':
            student.name = request.POST.get('name')
            student.age = request.POST.get('age')
            student.dob = request.POST.get('dob')
            student.address = request.POST.get('address')
            student.email = request.POST.get('email')
            student.parent_name = request.POST.get('parent_name')

            if 'image' in request.FILES:
                student.image = request.FILES['image']

            student.save()
            return redirect('Student:student_profile', student_id=student.id)
        
        return render(request, 'Student/edit_student_details.html', {'student': student})
    else:
        return redirect('Student:Login')
    


def update_password(request):
    Student_id = request.session.get('sid')
    if not Student_id:
        return redirect('Student:Login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        student = Student.objects.get(id=Student_id)

        if student.password == current_password and new_password == confirm_password:
            student.password = new_password  # Direct assignment; manage hashing elsewhere if needed
            student.save()
            return redirect('Student:student_profile', student_id=student.id)

    return render(request, 'Student/update_password.html')



def view_student_payments(request):
    student_id = request.session.get('sid')
    
    if student_id:
        student = Student.objects.get(id=student_id)
        payments = Payment.objects.filter(student=student)
        for payment in payments:
            payment.balance = payment.amount - payment.Paid_amount
        
        return render(request, 'Student/view_payments.html', {'student': student, 'payments': payments})
    else:
        return redirect('Student:Login')
