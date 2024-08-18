from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.files.storage import FileSystemStorage

from Administrator.models import ExamResult, Faculty
from Student.models import LeaveApplication
from .models import  AttendanceUpload, DisciplinaryRecord, Semester, Student, Subject
from .models import Parent
from .models import Student

# Create your views here.

def register_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        parent_name = request.POST.get('parent_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        
        # Handling image upload
        if request.FILES.get('image'):
            image = request.FILES['image']
            fs = FileSystemStorage()
            image_name = fs.save(image.name, image)
        else:
            image_name = None

        student = Student(
            name=name,
            age=age,
            dob=dob,
            email=email,
            image=image_name,
            parent_name=parent_name,
            password=password,
            address=address
        )
        student.save()

        return redirect('faculty:faculty_home')  # Replace with your success page or URL

    return render(request, 'faculty/Stud_reg.html')





def student_list(request):
    students = Student.objects.all()  # Retrieve all students from the database
    return render(request, 'faculty/view_Stud.html', {'students': students})





def register_parent(request):
    students = Student.objects.all()  # Get all students from the database

    if request.method == 'POST':
        student_id = request.POST.get('student_name')
        student = Student.objects.get(id=student_id)
        parent_name = request.POST.get('parent_name')
        parent_email = request.POST.get('parent_email')
        address = request.POST.get('address')
        password = request.POST.get('password')

        parent = Parent(student=student, parent_name=parent_name, parent_email=parent_email, address=address, password=password)
        parent.save()

        return redirect('faculty:faculty_home')  # Replace with your success page or URL

    return render(request, 'faculty/Parent_reg.html', {'students': students})








def enter_exam_result(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        semester_id = request.POST.get('semester_id')
        subject_marks = request.POST.getlist('subject_marks')  # List of marks
        subject_ids = request.POST.getlist('subject_ids')  # List of subject IDs

        student = Student.objects.get(id=student_id)
        semester = Semester.objects.get(id=semester_id)

        # Remove previous exam results for this student and semester
        ExamResult.objects.filter(student=student, semester=semester).delete()

        for subject_id, marks in zip(subject_ids, subject_marks):
            subject = Subject.objects.get(id=subject_id)
            exam_result = ExamResult(
                student=student,
                semester=semester,
                subject=subject,
                marks=marks
            )
            exam_result.save()

        return redirect('faculty:faculty_home')  # Replace with your success page or URL

    students = Student.objects.all()
    semesters = Semester.objects.all()

    return render(request, 'faculty/exam.html', {'students': students, 'semesters': semesters})
    
def load_subjects(request):
    semester_id = request.GET.get('semester_id')
    subjects = Subject.objects.filter(semester_id=semester_id).values('id', 'subject_name')
    return JsonResponse(list(subjects), safe=False)



def add_subjects(request):
    semesters = Semester.objects.all()

    if request.method == 'POST':
        semester_id = request.POST.get('semester_name')
        subject_name = request.POST.get('subject_name')

        semester = Semester.objects.get(id=semester_id)
        
        subject = Subject(
            semester=semester,
            subject_name=subject_name,
        )
        subject.save()

        return redirect('faculty:faculty_home')  # Replace with your success page or URL

    return render(request, 'faculty/Add_sub.html', {'semesters': semesters})




def add_disciplinary_record(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        disciplinary_action = request.POST.get('disciplinary_action')
        action_date = request.POST.get('action_date')

        student = Student.objects.get(id=student_id)

        DisciplinaryRecord.objects.create(
            student=student,
            disciplinary_action=disciplinary_action,
            action_date=action_date
        )

        return redirect('faculty:faculty_home')  # Replace with your success page or URL

    students = Student.objects.all()
    return render(request, 'faculty/Disp_form.html', {'students': students})

def faculty_home(request):
    faculty_id = request.session.get('fid')
    faculty_name = None
    
    if faculty_id:
        # Assuming you have a Faculty model with an id field and a name field
        faculty = Faculty.objects.get(id=faculty_id)
        faculty_name = faculty.name
    
    return render(request, 'faculty/fac_home.html', {'faculty_name': faculty_name})






def view_leave_applications(request):
    teacher_id = request.session.get('fid')

    if teacher_id:
        teacher = Faculty.objects.get(id=teacher_id)
        leave_applications = LeaveApplication.objects.filter(teacher=teacher)

        return render(request, 'faculty/view_leave.html', {
            'teacher': teacher,
            'leave_applications': leave_applications
        })
    else:
        return redirect('Student:Login')

def approve_leave(request, application_id):
    leave_application = get_object_or_404(LeaveApplication, id=application_id)
    leave_application.status = "Approved"
    leave_application.save()
    messages.success(request, f'Leave application for {leave_application.student.name} has been approved.')
    return redirect('faculty:view_leave_applications') # Redirect to teacher login if not authenticated
    


def faculty_profile(request):
    # Assuming the faculty's ID is stored in the session after login
    faculty_id = request.session.get('fid')  # Change 'tid' based on your session key

    if faculty_id:
        faculty = Faculty.objects.get(id=faculty_id)
        return render(request, 'faculty/Fac_profile.html', {'faculty': faculty})
    else:
        return redirect('Student:Login') 
    

def edit_profile(request):
    faculty_id = request.session.get('fid')
    if not faculty_id:
        return redirect('Teacher:Login')

    faculty = Faculty.objects.get(id=faculty_id)
    if request.method == 'POST':
        faculty.name = request.POST.get('name')
        faculty.dob = request.POST.get('dob')
        faculty.email = request.POST.get('email')
        faculty.phone = request.POST.get('phone')
        faculty.gender = request.POST.get('gender')
        faculty.department = request.POST.get('department')
        faculty.qualification = request.POST.get('qualification')
        faculty.experience = request.POST.get('experience')
        faculty.save()
        return redirect('faculty:faculty_profile')

    return render(request, 'faculty/Edit_profile.html', {'faculty': faculty})




def update_password(request):
    faculty_id = request.session.get('fid')
    if not faculty_id:
        return redirect('Student:Login')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        faculty = Faculty.objects.get(id=faculty_id)

        if faculty.password == current_password and new_password == confirm_password:
            faculty.password = new_password  # Direct assignment; manage hashing elsewhere if needed
            faculty.save()
            return redirect('faculty:faculty_profile')

    return render(request, 'faculty/Update_password.html')




def upload_attendance(request):
    if request.method == 'POST':
        # Handle file upload
        attendance_file = request.FILES.get('attendance_file')

        if attendance_file:
            # Save the uploaded file to the model
            AttendanceUpload.objects.create(file=attendance_file)
            return redirect('faculty:faculty_home')  # Redirect after successful upload

    return render(request, 'faculty/Attendance.html')