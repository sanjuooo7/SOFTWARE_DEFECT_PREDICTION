import smtplib
from email.mime.text import MIMEText
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.
from my_app.Prediction_file import random_forest
from my_app.models import *





def login(request):
    request.session['lid']=""
    return render(request, 'index.html')
def login_post(request):
    btn=request.POST['btn']
    if btn=="Login":
        try:
            username=request.POST['username']
            password=request.POST['password']
            a=Login.objects.get(username=username,password=password)
            request.session['lid'] = a.id
            if a.type=='admin':
                ob1 = auth.authenticate(username='admin', password='admin')
                if ob1 is not None:
                    auth.login(request, ob1)
                return HttpResponse('''<script>alert('Admin logged in ...');window.location='/home'</script>''')
            elif a.type=='expert':
                ob1 = auth.authenticate(username='admin', password='admin')
                if ob1 is not None:
                    auth.login(request, ob1)
                kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
                pp = len(kk)
                print(pp, "kkkkkkkkkkkkkkkkkkk")

                request.session['co']=pp
                return HttpResponse('''<script>alert('Expert logged in ...');window.location='/experthome'</script>''')
            elif a.type=='user':
                ob1 = auth.authenticate (username='admin', password='admin')
                if ob1 is not None:
                    auth.login(request, ob1)
                return HttpResponse('''<script>alert('User logged in ...');window.location='/user_home'</script>''')
            else:
                return HttpResponse('''<script>alert(' Your Are in Waiting List ...');window.location='/'</script>''')
        except:
                return HttpResponse('''<script>alert(' Your Are in Waiting List ...');window.location='/'</script>''')
    else:
        return render(request, 'forgot_psw.html')




@login_required(login_url='/')
def view_expert(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=Expert.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/man_experts.html', {'data': a, 'user_count': up, 'expert_count': ep})
    # return  render(request,'admin/man_experts.html',{'data':a})

def accept_expert(request,id):
    request.session['eid']=id
    ob=Login.objects.get(id=id)
    ob.type='expert'
    ob.save()
    obe=Expert.objects.get(login_id__id=id)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText(" We are pleased to inform you that after careful evaluation of your application and interview performance, we have selected you for the role of Software Expert. Congratulations!!! Your technical expertise and problem-solving abilities have impressed our team, and we believe you will be a great addition to our organization.")
    print(msg)
    msg['Subject'] = 'Acceptance Email - Congratulations!!!'
    msg['To'] = obe.email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        pass
    return HttpResponse('''<script>alert(' Accepted ...');window.location='/view_expert'</script>''')

def reject_expert(request,id):
    request.session['eid']=id

    obe = Expert.objects.get(login_id__id=id)
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText(" Dear Candidate,Thank you for taking the time to apply for the Software Expert role at [Company Name]. We truly appreciate your interest and the effort you put into the application and interview process.After careful consideration, we regret to inform you that we have chosen to proceed with another candidate at this time. This decision was not an easy one, as we received applications from many highly qualified professionals, including yourself. ")
    print(msg)
    msg['Subject'] = 'Rejection Email - Thank You for Your Application'
    msg['To'] = obe.email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        pass
    ob = Login.objects.get(id=id)
    ob.type = 'reject'
    ob.delete()
    return HttpResponse('''<script>alert(' rejected ...');window.location='/view_expert'</script>''')

@login_required(login_url='/')
def home(request):
    a=User.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/index.html', {'data': a, 'user_count': up, 'expert_count': ep})

@login_required(login_url='/')
def user_home(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=User.objects.all()

    return render(request,'user/index.html',{'data':a})

@login_required(login_url='/')
def admin_home(request):
    a=User.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep=len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request,'admin/index.html',{'data':a,'user_count': up,'expert_count': ep})

@login_required(login_url='/')
def expert_home(request):
    a=User.objects.all()
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return render(request,'expert/index.html',{'data':a})


@login_required(login_url='/')
def view_users(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=User.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/view_users.html', {'data': a, 'user_count': up, 'expert_count': ep})
    # return  render(request,'admin/view_users.html',{'data':a})

@login_required(login_url='/')
def block_user(request,id):
    request.session['eid']=id
    ob=Login.objects.get(id=id)
    ob.type='block'
    ob.save()
    return HttpResponse('''<script>alert(' user is blocked ...');window.location='/view_users'</script>''')

@login_required(login_url='/')
def unblock_user(request,id):
    request.session['eid']=id
    ob=Login.objects.get(id=id)
    ob.type='user'
    ob.save()
    return HttpResponse('''<script>alert(' user is unblocked ...');window.location='/view_users'</script>''')



@login_required(login_url='/')
def send_notifications(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    return  render(request,'admin/send_notifications.html')

@login_required(login_url='/')
def send_notification_post(request):
    notification=request.POST['notification']
    type=request.POST['type']
    ob=Admin_Notification()
    ob.notification=notification
    ob.type=type
    ob.date = datetime.datetime.now()
    ob.save()
    return HttpResponse("<script>alert(' Notification Sent Successfully');window.location='/home#aa'</script>")

# expert
@login_required(login_url='/')
def view_adm_notifications(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=Admin_Notification.objects.filter(type='expert')
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    # return render(request, 'admin/index.html', {'data': a, 'user_count': up, 'expert_count': ep})
    return  render(request,'expert/view_adm_notifications.html',{'val':a, 'user_count': up, 'expert_count': ep})


@login_required(login_url='/')
def view_complaints(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=Complaint.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/view_complaints.html', {'data': a, 'user_count': up, 'expert_count': ep})
    # return  render(request,'admin/view_complaints.html',{'data':a})

@login_required(login_url='/')
def send_reply(request,id):
    request.session['cid']=id
    return  render(request,'admin/send_reply.html')

@login_required(login_url='/')
def view_feedback(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=Feedback.objects.all()
    user_count = User.objects.all()  # Count total registered users
    up = len(user_count)
    expert_count = Expert.objects.all()  # Count total registered Experts
    ep = len(expert_count)
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/view_feedback.html', {'data': a, 'user_count': up, 'expert_count': ep})
    # return  render(request,'admin/view_feedback.html',{'data':a})

def logout(request):
    auth.logout(request)
    return render(request,'index.html')

def signup_user(request):
    return render(request,'user_reg.html')

def signup_expert(request):
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return render(request,'expert_reg.html')

@login_required(login_url='/')
def view_result(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    return render(request,'view_result.html')

def user_reg(request):
    # if request.method == "POST":
    return render(request,'u ser_reg.html')



# user
@login_required(login_url='/')
def send_complaints(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    ob=Complaint.objects.filter(user_id__login_id=request.session["lid"])
    return render(request,'user/send_complaints.html',{"data":ob})

@login_required(login_url='/')
def send_complaints_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    comp=request.POST["comp"]

    ob=Complaint()
    ob.complaint=comp
    ob.date=datetime.datetime.now().date()
    ob.reply="pending"
    ob.user_id=User.objects.get(login_id=request.session["lid"])
    ob.save()
    return HttpResponse("<script>alert('Complaint Sent Successfully');window.location='/user_home'</script>")


@login_required(login_url='/')
def send_reply_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    reply=request.POST["reply"]

    ob=Complaint.objects.get(id=request.session['cid'])
    ob.reply=reply
    ob.date=datetime.datetime.now()
    ob.save()
    return HttpResponse("<script>alert('Reply Sent Successfully');window.location='/view_complaints#aa'</script>")




@login_required(login_url='/')
def send_feedback(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    return render(request,'user/send_feedback.html')

@login_required(login_url='/')
def send_feedback_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    feedback=request.POST["comment"]
    rating=request.POST["satisfaction"]

    ob=Feedback()
    ob.feedback=feedback
    ob.rating=rating
    ob.date=datetime.datetime.now()
    ob.user_id=User.objects.get(login_id=request.session['lid'])
    ob.save()
    return HttpResponse("<script>alert('Feedback Submitted Successfully');window.location='/user_home'</script>")



# CHAT
@login_required(login_url='/')
def chatwithuser(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    ob = Expert.objects.all()
    return render(request, "user/fur_chatt.html", {'val':ob})



@login_required(login_url='/')
def chatview(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    ob = Expert.objects.all()
    d=[]
    for i in ob:
        r={"name":i.expert_name,'photo':i.photo.url,'email':i.email,'loginid':i.login_id.id}
        d.append(r)
    from django.http import JsonResponse
    return JsonResponse(d, safe=False)




def coun_insert_chat(request,msg,id):
    print("===",msg,id)
    ob=Chat()
    ob.from_id=Login.objects.get(id=request.session['lid'])
    ob.to_id=Login.objects.get(id=id)
    ob.chat=msg
    ob.status='pending'
    import datetime
    ob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    ob.save()

    from django.http import JsonResponse
    return JsonResponse({"task":"ok"})
    # refresh messages chatlist


@login_required(login_url='/')
def coun_msg(request,id):

    ob1=Chat.objects.filter(from_id__id=id,to_id_id=request.session['lid'])
    ob2=Chat.objects.filter(from_id_id=request.session['lid'],to_id__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.from_id.id,"msg":i.chat,"date":i.date,"chat_id":i.id})

    obu=Expert.objects.get(login_id_id=id)

    from django.http import JsonResponse
    return JsonResponse({"data":res,"name":obu.expert_name,"photo":obu.photo.url,"user_lid":obu.login_id.id})

@login_required(login_url='/')
# ----------------chat with user----------------------
def chatwithetouser(request):
    ob = User.objects.all()
    kk=Chat.objects.filter(to_id__id=request.session['lid'],status='pending')
    for i in kk:
        i.status='viewed'
        i.save()
    request.session['co']=0
    return render(request, "expert/fur_chat.html", {'val':ob})


@login_required(login_url='/')
def chatviewExpert(request):
    ob = User.objects.all()
    d=[]
    for i in ob:
        kk=Chat.objects.filter(from_id__id=i.login_id.id,to_id__id=request.session['lid'],status='pending')
        pp=len(kk)
        r={"name":i.name,'photo':i.photo.url,'email':i.email,'loginid':i.login_id.id,"pp":pp}
        d.append(r)
    from django.http import JsonResponse
    return JsonResponse(d, safe=False)



@login_required(login_url='/')
def coun_insert_chatExpert(request,msg,id):
    print("===",msg,id)
    ob=Chat()
    ob.from_id=Login.objects.get(id=request.session['lid'])
    ob.to_id=Login.objects.get(id=id)
    ob.chat=msg
    ob.status="pending"
    import datetime
    ob.date=datetime.datetime.now().strftime("%Y-%m-%d")
    ob.save()

    from django.http import JsonResponse
    return JsonResponse({"task":"ok"})
    # refresh messages chatlist


@login_required(login_url='/')
def coun_msgExpert(request,id):

    ob1=Chat.objects.filter(from_id__id=id,to_id_id=request.session['lid'])
    ob2=Chat.objects.filter(from_id_id=request.session['lid'],to_id__id=id)
    combined_chat = ob1.union(ob2)
    combined_chat=combined_chat.order_by('id')
    res=[]
    for i in combined_chat:
        res.append({"from_id":i.from_id.id,"msg":i.chat,"date":i.date,"chat_id":i.id})

    obu=User.objects.get(login_id_id=id)

    from django.http import JsonResponse
    return JsonResponse({"data":res,"name":obu.name,"photo":obu.photo.url,"user_lid":obu.login_id.id})




def user_reg_post(request):
    print(request.POST)
    image=request.FILES['image']
    name=request.POST['name']
    gender=request.POST['gender']
    dob=request.POST['dob']
    email=request.POST['email']
    place=request.POST['place']
    phone=request.POST['phone']
    pin=request.POST['pin']
    username=request.POST['username']
    password=request.POST['password']

    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    a=Login()
    a.username=username
    a.password=password
    a.type='user'
    a.save()


    b=User()
    b.login_id=a
    b.name=name
    b.gender=gender
    b.dob=dob
    b.email=email
    b.place=place
    b.phone=phone
    b.pin=pin
    b.photo=path
    b.save()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Below are your login details:\n Username: "+a.username +"\n Password: "+a.password)
    print(msg)
    msg['Subject'] = 'Password for Your Account'
    msg['To'] = email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        print(e)
        pass
    # return HttpResponse('''<script>alert('REGISTERED SUCCESSFULLY  ...  \n  USERNAME & PASSWORD has been sent to mail Successfully');window.location='/'</script>''')
    return HttpResponse('''<script>alert('REGISTERED SUCCESSFULLY USERNAME & PASSWORD has been sent to mail Successfully  ... ');window.location='/'</script>''')


def expert_reg(request):
    # if request.method == "POST":
    # kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    # pp = len(kk)
    # print(pp, "kkkkkkkkkkkkkkkkkkk")
    #
    # request.session['co'] = pp
    return render(request,'expert_reg.html')


def expert_reg_post(request):
    print(request.POST)
    expert_name=request.POST['name']
    place=request.POST['place']
    gender=request.POST['gender']
    email=request.POST['email']
    phone=request.POST['phone']
    experience=request.POST['experience']
    qualification=request.POST['qualification']
    image=request.FILES['image']
    username=request.POST['username']
    password=request.POST['password']

    fs=FileSystemStorage()
    path=fs.save(image.name,image)

    a=Login()
    a.username=username
    a.password=password
    a.type='pending'
    a.save()


    b=Expert()
    b.login_id=a
    b.expert_name=expert_name
    b.gender=gender
    b.experience=experience
    b.email=email
    b.place=place
    b.phone=phone
    b.qualification=qualification
    b.photo=path
    b.save()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Below are your login details:\n Username: " + a.username + "\n Password: " + a.password)
    print(msg)
    msg['Subject'] = 'Password for Your Account'
    msg['To'] = email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        print(e)
        pass
    # return HttpResponse('''<script>alert('REGISTERED SUCCESSFULLY  ...  \n  USERNAME & PASSWORD has been sent to mail Successfully');window.location='/'</script>''')
    return HttpResponse(
        '''<script>alert('REGISTERED SUCCESSFULLY USERNAME & PASSWORD has been sent to mail Successfully  ... ');window.location='/'</script>''')
    return HttpResponse('''<script>alert(' EXPERT REGISTERED SUCCESSFULLY ...');window.location='/'</script>''')


@login_required(login_url='/')
def experthome(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return render(request,'expert/index.html')

@login_required(login_url='/')
def ex_send_notifications(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=Notification.objects.all()
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return  render(request,'expert/ex_send_notifications.html',{'data':a})

@login_required(login_url='/')
def ex_send_notifications_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    notification=request.POST["notification"]
    ob=Notification()
    ob.expert_id=Expert.objects.get(login_id_id=request.session['lid'])
    ob.notification=notification
    ob.date=datetime.datetime.now()
    ob.save()
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return HttpResponse("<script>alert('Notification Sent Successfully');window.location='/experthome'</script>")

# send_reply_post(request):
#     reply=request.POST["reply"]
#
#     ob=Complaint.objects.get(id=request.session['cid'])
#     ob.reply=reply
#     ob.date=datetime.datetime.now()
#     ob.save()
#     return HttpResponse("<script>alert('Reply Sent Successfully');window.location='/view_complaints#aa'</script>")



# expert
@login_required(login_url='/')
def view_user_req(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a=User.objects.all()
    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return  render(request,'expert/view_user_req.html',{'data':a})

# user

@login_required(login_url='/')
def user_view_notifications(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    a = Notification.objects.all()
    b = Admin_Notification.objects.filter(type='user')
    return render(request, 'user/view_notifications.html', {'data': a,'val': b})

@login_required(login_url='/')
def user_view_admin_notifications(request):
    b = Admin_Notification.objects.filter(type== 'user')
    return render(request, 'user/view_notifications.html', {'val': b})


@login_required(login_url='/')
def manage_dataset(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    return  render(request,'expert/manage_dataset.html')

@login_required(login_url='/')
def pred_input(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    return render(request,'user/pred_input.html')

@login_required(login_url='/')
def pred_input_post(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')


    print(request.POST)


    loc = float(request.POST["loc"])
    v_g = float(request.POST["v_g"])
    ev_g = float(request.POST["ev_g"])
    iv_g = float(request.POST["iv_g"])
    n = float(request.POST["n"])
    v = float(request.POST["v"])
    l = float(request.POST["l"])
    d = float(request.POST["d"])
    i = float(request.POST["i"])
    e = float(request.POST["e"])
    b = float(request.POST["b"])
    t = float(request.POST["t"])

    lOCode = float(request.POST["lOCode"])
    lOComment = float(request.POST["lOComment"])
    lOBlank = float(request.POST["lOBlank"])
    lOCodeAndComment = float(request.POST["lOCodeAndComment"])
    uniq_Op = float(request.POST["uniq_Op"])
    uniq_Opnd = float(request.POST["uniq_Opnd"])
    total_Op = float(request.POST["total_Op"])
    total_Opnd = float(request.POST["total_Opnd"])
    branchCount = float(request.POST["branchCount"])



    ob=random_forest(loc,v_g,ev_g,iv_g,n,v,l,d,i,e,b,t,lOCode,lOComment,lOBlank,lOCodeAndComment,uniq_Op,uniq_Opnd,total_Op,total_Opnd,branchCount)


    print("Result=============",ob)
    return render(request,'user/view_result.html',{"res": ob,"loc": loc,"v_g": v_g,"ev_g": ev_g,"iv_g": iv_g,"n": n,"v": v,"l": l,"d": d,"i": i,"e": e,"b": b,"t": t,"lOCode": lOCode,"lOComment": lOComment,"lOBlank": lOBlank,"lOCodeAndComment": lOCodeAndComment,"uniq_Op": uniq_Op,"uniq_Opnd": uniq_Opnd,"total_Op": total_Op,"total_Opnd": total_Opnd,"branchCount": branchCount,})

@login_required(login_url='/')
def chat_with_expert2(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')


    return render(request,'user/fur_chatt.html')

@login_required(login_url='/')
def delete_complaints(request,id):

    request.session['cid']=id
    ob=Complaint.objects.get(id=id)
    ob.delete()
    return HttpResponse("<script>alert(' Complaint deleted Successfully');window.location='/view_complaints'</script>")


import csv
@login_required(login_url='/')
def insert_data(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    data = [
        float(request.POST.get("loc", 0)),
        float(request.POST.get("v_g", 0)),
        float(request.POST.get("ev_g", 0)),
        float(request.POST.get("iv_g", 0)),
        float(request.POST.get("n", 0)),
        float(request.POST.get("v", 0)),
        float(request.POST.get("l", 0)),
        float(request.POST.get("d", 0)),
        float(request.POST.get("i", 0)),
        float(request.POST.get("e", 0)),
        float(request.POST.get("b", 0)),
        float(request.POST.get("t", 0)),

        float(request.POST.get("lOCode", 0)),
        float(request.POST.get("lOComment", 0)),
        float(request.POST.get("lOBlank", 0)),
        float(request.POST.get("lOCodeAndComment", 0)),
        float(request.POST.get("uniq_Op", 0)),
        float(request.POST.get("uniq_Opnd", 0)),
        float(request.POST.get("total_Op", 0)),
        float(request.POST.get("total_Opnd", 0)),
        float(request.POST.get("branchCount", 0)),
    ]
    print(request.GET)
    true_false_choice = request.POST['true_false_choice']
    data.append(true_false_choice)  # Append True or False value to the dataset



    csv_file = r"C:\Users\hp\PycharmProjects\myproject\my_app\jm1.csv"

    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write headers if the file is empty
        if file.tell() == 0:
            writer.writerow(["LOC", "V(G)", "EV(G)", "IV(G)", "N", "V", "L", "D", "I", "E", "B", "T"])

        # Write data row
        writer.writerow(data)

    print("Data inserted successfully into CSV.")
    # return render(request,'expert/manage_dataset.html')
    return HttpResponse("<script>alert('Inserted Successfully');window.location='/manage_dataset'</script>")


@login_required(login_url='/')
def view_dataset(request):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    kk = Chat.objects.filter(to_id__id=request.session['lid'], status='pending')
    pp = len(kk)
    print(pp, "kkkkkkkkkkkkkkkkkkk")

    request.session['co'] = pp
    csv_file = r"C:\Users\hp\PycharmProjects\myproject\my_app\jm1.csv"

    # Open and read the file
    with open(csv_file, "r", newline="") as file:
        response = HttpResponse(file, content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{csv_file}"'
        return response


def forgot_psw(request):
    return render(request, 'forgot_psw.html')


def forgot_psw_post(request):
    email = request.POST['email']
    ob=User.objects.get(email=email)
    ob.save()
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("We received a request to reset your password for your account associated with this email address. Below are your login details:\n Username: "+ob.login_id.username +"\n Password: "+ob.login_id.password)
    print(msg)
    msg['Subject'] = 'Password for Your Account'
    msg['To'] = email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        print(e)
        pass
    return HttpResponse("<script>alert('Password sent to mail Successfully');window.location='/'</script>")


@login_required(login_url='/')
def delete_expert(request,id):
    if request.session['lid']=="":
        return HttpResponse('''<script>alert(' SESSION EXPIRED PLEASE LOGIN  ');window.location='/'</script>''')

    request.session['cid']=id
    ob=Login.objects.get(id=id)
    obe=Expert.objects.get(login_id__id=id)

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hibamuhsinakm8005@gmail.com', 'pkpolwistnzbayfr')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("  deleted ")
    print(msg)
    msg['Subject'] = 'Removed your position '
    msg['To'] = obe.email
    msg['From'] = 'hibamuhsinakm8005@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        pass

    ob.delete()

    return HttpResponse("<script>alert(' Expert deleted Successfully');window.location='/view_expert'</script>")


@login_required(login_url='/')
def admin_dashboard(request):
    user_count = User.objects.count()  # Count total registered users
    expert_count = Expert.objects.count()  # Count total registered Experts
    print("User Count:", user_count)  # Debugging step
    print("Expert Count:", expert_count)  # Debugging step
    return render(request, 'admin/index.html', {'user_count': user_count},{'expert_count': expert_count})
