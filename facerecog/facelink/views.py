import base64
import datetime
import glob
import os
from io import BytesIO

import numpy as np
from deepface import DeepFace
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .models import *


# Create your views here.
def index(request):
    return redirect(contact)

def signup(request):
    if request.method=='POST':
        f=request.POST['f_name']
        l=request.POST['l_name']
        usern=request.POST['username']
        dep=request.POST['department']
        image=request.FILES['image']
        email=request.POST['email']
        pas=request.POST['password']
        cpas=request.POST['c-password']

        if pas==cpas:
            user=None
            if User.objects.filter(username=usern).exists():
                user=User.objects.get(username=usern)
                if signup_page.objects.filter(userr=user).exists():
                    print("Already exists")
                    g={'key':'User already exist'}
                    return render(request,"signup.html",g)
            else:
                User.objects.create_user(username=usern,password=pas).save()
                user=User.objects.get(username=usern)
            if user:
                if signup_page.objects.filter(user_name=usern).exists():
                    f={'key':'User name already exists'}
                    return render(request,"signup.html",f)
                else:
                    u=signup_page(userr=user, f_name=f, l_name=l, user_name=usern, department=dep, image=image, email=email, password=pas)
                    u.save()
                    print(u)
                    print("saved successfully")
                    return redirect(login)
        else:
            m={'key':'password incorrect'}
            return render(request,"signup.html",m)
    else:
        return render(request,"signup.html")
    return render(request,"signup.html")

@login_required
def show(request,pk):
    b=signup_page.objects.get(id=pk)
    f={'key':b}
    return render(request,"view.html",f)

@login_required
def view1(request):
    logged_in_teacher=get_logged_in_teacher(request.user)
    students=signup_page.objects.filter(department=logged_in_teacher.department)
    d={'view':students}
    return render(request,"formview.html",d)

def get_logged_in_teacher(user):
    try:
        return fac_sign.objects.get(userr=user)
    except fac_sign.DoesNotExist:
        return None

@login_required
def update(request,lm):
    a=signup_page.objects.get(id=lm)
    if request.method=="POST":
        a.f_name=request.POST["uf_name"]
        a.l_name=request.POST["ul_name"]
        a.user_name=request.POST["u_nam"]
        a.department=request.POST["u_dep"]
        a.email=request.POST["u_email"]
        a.password=request.POST["u_pass"]
        a.save()
        return redirect(profile)
    return render(request,'update.html',{"key":a})

@login_required
def delete(request,pk):
    a=signup_page.objects.get(id=pk)
    image=a.image

    try:
        b=student_page.objects.get(userr_id=a.userr_id)
        b.delete()
    except student_page.DoesNotExist:
        b=None

    import os
    location = os.getcwd()
    path = os.path.join(location, str(image))

    a.delete()
    os.remove(path)
    return redirect(view1)

def login(request):
    if request.method=='POST':
        u=request.POST['username']
        p=request.POST['password']
        if signup_page.objects.filter(user_name=u,password=p).exists():
            a=auth.authenticate(username=u,password=p)
            if a is not None:
                auth.login(request,a)
                print('successfully login')
                return redirect(second)
            else:
                f={'key':'Invalid Data Entered'}
                return render(request,"login.html",f)
        else:
            print("Not found")
            g={'key':'User not found'}
            return render(request,"login.html",g)
    return render(request,"login.html")

def greet(user):
    return fac_sign.objects.get(userr=user)

def main(request):
    tea=greet(request.user)
    t={'key':tea.name}
    return render(request,"main.html",t)

def stgreet(user):
    return signup_page.objects.get(userr=user)

def second(request):
    tea=stgreet(request.user)
    t={'key':tea.f_name+' '+tea.l_name}
    return render(request,"second.html",t)


def fac_signup(request):
    if request.method=='POST':
        f=request.POST['name']
        usern=request.POST['username']
        dep=request.POST['department']
        image=request.FILES['image']
        email=request.POST['email']
        n=request.POST['number']
        pas=request.POST['password']
        cpas=request.POST['c-password']
        if pas==cpas:
            user=None
            if User.objects.filter(username=usern).exists():
                user=User.objects.get(username=usern)
                if fac_sign.objects.filter(userr=user).exists():
                    print("Already exists")
                    k={'key':'User already exist'}
                    return render(request,"faculty_signup.html",k)
            else:
                User.objects.create_user(username=usern,password=pas).save()
                user=User.objects.get(username=usern)
            if user:
                if fac_sign.objects.filter(user_name=usern).exists():
                    f={'key':'User name already exists'}
                    return render(request,"faculty_signup.html",f)
                else:
                    fac_sign(userr=user,name=f,user_name=usern,department=dep,image=image,email=email,number=n,password=pas).save()
                    print("saved successfully")
                    return redirect(faclogin)
        else:
            m={'key':'password incorrect'}
            return render(request,"faculty_signup.html",m)
    else:
        return render(request,"faculty_signup.html")
    return render(request,"faculty_signup.html")

def faclogin(request):
    if request.method=='POST':
        u=request.POST['username']
        p=request.POST['password']
        if fac_sign.objects.filter(user_name=u,password=p).exists():
            a=auth.authenticate(username=u,password=p)
            if a is not None:
                auth.login(request,a)
                print('successfully login')
                return redirect(main)
            else:
                f={'key':'Invalid Data Entered'}
                return render(request,"faclogin.html",f)
        else:
            print("Not found")
            g={'key':'User not found'}
            return render(request,"faclogin.html",g)
    return render(request,"faclogin.html")

def getout(request):
    logout(request)
    return redirect('/')

def contact(request):
    g={'key':'+91 9400628129','key2':'+91 9672812923','key3':'Email: facelinkcor09@gmail.com'}
    return render(request,"index.html",g)

@login_required
def profile(request):
    a=request.user
    b=signup_page.objects.filter(userr=a).all()
    c={'key':b}
    return render(request,"profile.html",c)

@login_required
def twoprofile(request):
    a=request.user
    b=fac_sign.objects.filter(userr=a).all()
    c={'key':b}
    return render(request,"twoprofile.html",c)

@login_required
def tea_update(request,pk):
    a=fac_sign.objects.get(id=pk)
    if request.method=="POST":
        a.name=request.POST["uf_name"]
        a.user_name=request.POST["ul_name"]
        a.department=request.POST["u_dep"]
        a.email=request.POST["u_email"]
        a.number=request.POST["u_num"]
        a.password=request.POST["u_pass"]
        a.save()
        return redirect(twoprofile)
    return render(request,'teach_update.html',{"key":a})

@login_required
def biodata(request):
    user=request.user
    try:
        studsign=signup_page.objects.get(userr=user)
        studdet=student_page.objects.get(userr=user)
        context={'stdsign':studsign,'stddet':studdet}
        return render(request,'biodata.html',context)
    except student_page.DoesNotExist:
        return HttpResponseBadRequest("<style>b{color:red;font-size:100px;}</style><b>You are not still add details.</b>")

@login_required
def details(request):
    if request.method == 'POST':
        user=request.user
        ad=request.POST['adm_num']
        dob=request.POST['dob']
        fath=request.POST['father']
        moth=request.POST['mother']
        n=request.POST['number']
        gen=request.POST['gender']
        age=request.POST['age']
        inc=request.POST['income']
        rel=request.POST['radio-buttons']
        caste=request.POST['caste']
        bg=request.POST['bgroup']
        addr=request.POST['address']
        dis=request.POST['district']
        st=request.POST['state']
        lang=request.POST['prefer']
        nat=request.POST['nation']

        studdet, created= student_page.objects.get_or_create(userr=user)
        studdet.adm_no=ad
        studdet.dob=dob
        studdet.father=fath
        studdet.mother=moth
        studdet.number=n
        studdet.gender=gen
        studdet.age=age
        studdet.income=inc
        studdet.religion=rel
        studdet.caste=caste
        studdet.bloodgroup=bg
        studdet.address=addr
        studdet.district=dis
        studdet.state=st
        studdet.lang=lang
        studdet.nation=nat
        studdet.save()

        return redirect(biodata)
    return render(request,'details.html')

def trim_fun(stri):
    ind=stri.find(".jpg")
    if ind !=-1:
        sli=stri[:ind+4]
        return sli
    else:
        return stri
    
# Define a function to recognize faces
def recognize_faces(face_image):
    image_file = Image.open(BytesIO(base64.b64decode(face_image.split(',')[1])))
    if image_file is None:
        return HttpResponseBadRequest("Failed to read the image.")
    
    file_path="profile_pic/representations_facenet512.pkl"
    if os.path.exists(file_path):
        os.remove(file_path)
    # Recognize faces in the image
    img1_path = np.array(image_file)
    db = 'profile_pic'
    results = DeepFace.find(img1_path, db_path=db, model_name='Facenet512')
    ch_path=results[0]['identity']
    match_path=str(ch_path)
    path_c=match_path[5:]
    h_path= trim_fun(path_c)
    if h_path:
        try:
            match_entry = signup_page.objects.get(image=h_path)
        except signup_page.DoesNotExist:
            return HttpResponseBadRequest("Image with name  not found in signup_page database.")
        user = match_entry.userr_id
        return user
    else:
        return None


@csrf_exempt
def face_recognition(request):
    if request.method == 'POST':
        # Get the uploaded image
        image_data = request.POST.get('image-data')
        if not image_data:
            return HttpResponseBadRequest("Image data is missing.")
        userid = recognize_faces(image_data)
        try:
            user_instance = User.objects.get(id=userid)
            if user_instance:
                attendance_records = FaceRecognition.objects.filter(userr=user_instance, date=datetime.date.today())
                if attendance_records.exists():
                    messages.error(request, "Attendance for today is already marked.")
                    return redirect(failure)
                else:
                    attendance = FaceRecognition.objects.create(userr=user_instance, date=datetime.date.today())
                    attendance.attendance = True
                    attendance.save()
                    a=signup_page.objects.get(userr=user_instance)
                    a={'key':a}
                    return render(request,"success.html",a)
        except FaceRecognition.DoesNotExist:
                return HttpResponseBadRequest("Failed to mark attendance")
    else:
        return render(request, 'face_recognition.html')    

def failure(request):
    return render(request,"failure.html")

@login_required
def generate_pdf(request):
    user = request.user
    try:
        studsign = signup_page.objects.get(userr=user)
        stddet = student_page.objects.get(userr=user)

        # Generate the PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("Biodata", styles["Title"]),
            Spacer(1, 12),
            Paragraph("Name: {} {}".format(studsign.f_name, studsign.l_name), styles["Heading2"]),
            Paragraph("Department: {}".format(studsign.department), styles["Heading3"]),
            Paragraph("Email: {}".format(studsign.email), styles["Heading3"]),
            Paragraph("Admission Number: {}".format(stddet.adm_no), styles["Heading3"]),
            Paragraph("Date of Birth: {}".format(stddet.dob), styles["Heading3"]),
            Paragraph("Father's Name: {}".format(stddet.father), styles["Heading3"]),
            Paragraph("Mother's Name: {}".format(stddet.mother), styles["Heading3"]),
            Paragraph("Number: {}".format(stddet.number), styles["Heading3"]),
            Paragraph("Gender: {}".format(stddet.gender), styles["Heading3"]),
            Paragraph("Age: {}".format(stddet.age), styles["Heading3"]),
            Paragraph("Income: {}".format(stddet.income), styles["Heading3"]),
            Paragraph("Religion: {}".format(stddet.religion), styles["Heading3"]),
            Paragraph("Caste: {}".format(stddet.caste), styles["Heading3"]),
            Paragraph("Blood Group: {}".format(stddet.bloodgroup), styles["Heading3"]),
            Paragraph("Address: {}".format(stddet.address), styles["Heading3"]),
            Paragraph("District: {}".format(stddet.district), styles["Heading3"]),
            Paragraph("State: {}".format(stddet.state), styles["Heading3"]),
            Paragraph("Preferred Language: {}".format(stddet.lang), styles["Heading3"]),
            Paragraph("Nationality: {}".format(stddet.nation), styles["Heading3"]),
        ]
        doc.build(elements)

        # Save the PDF to a file
        file_path = os.path.join(settings.MEDIA_ROOT, 'biodata.pdf')
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())

        # Provide a download link to the user
        download_link = f'<a style="color:green;font-weight:bolder;font-size: 90px;border: solid black;text-decoration: none;text-transform: uppercase;" href="{settings.MEDIA_URL}biodata.pdf">Download Biodata PDF</a>'
        return HttpResponse(download_link)

    except ObjectDoesNotExist:
        return HttpResponseBadRequest("<style>b{color:red;font-size:100px;}</style><b>You have not added details yet.</b>")
    

@login_required
def scholarship_list(request):
    try:
        user=request.user
        student = student_page.objects.get(userr=user)
        # Query scholarships based on criteria
        scholarships = Scholarship.objects.all()
        context = {
        'scholarships': scholarships,
        'student':student
        }
        return render(request, 'scholarship_list.html', context)
    except student_page.DoesNotExist:
        return HttpResponseBadRequest("<style>b{color:red;font-size:100px;}</style><b>You have not added details yet.</b>")

@login_required
def present(request,pk):
    try:
        today= datetime.date.today()
        a=FaceRecognition.objects.get(userr=pk,date=today)
        b=signup_page.objects.get(userr=pk)
        c=student_page.objects.get(userr=pk)
        if request.method=="POST":
            a.attendance=request.POST["attend_mark"]
            a.save()
        m={'key':a,'key2':b,'key3':c}
        return render(request,'attendance.html',m)
    except FaceRecognition.DoesNotExist:
        return HttpResponseBadRequest("<style>b{color:red;font-size:100px;}</style><b>He is absent today...</b>")
    
def overall_attendance(request):
    today = datetime.date.today()
    registered_students = signup_page.objects.filter(userr__isnull=False)
    total_students = registered_students.count()
    present_students = FaceRecognition.objects.filter(date=today, attendance=True)
    present_students_count = present_students.count()

    # Get the names and register numbers of present students
    present_students_list = []
    for student in present_students:
        user = student.userr
        try:
            signup = signup_page.objects.get(userr=user)
            st_page = student_page.objects.get(userr=user)
            present_students_list.append({
                'name': f"{signup.f_name} {signup.l_name}",
                'reg_num': st_page.adm_no,
            })
        except signup_page.DoesNotExist:
            pass

    context = {
        'registered_students': registered_students,
        'total_students': total_students,
        'present_students': present_students,
        'present_students_count': present_students_count,
        'present_students_list': present_students_list,
    }
    return render(request, 'overall_attendance.html', context)