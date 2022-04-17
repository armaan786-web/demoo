from http import client
from unicodedata import category
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from studentapp.EmailBackend import EmailBackend
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from studentapp .models import Course,Staff , CustomUser,order
from django.contrib.auth.decorators import login_required
from studentapp.models import *
from django.views.decorators.csrf import csrf_exempt
import razorpay
client =razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
from django.urls import reverse
from django.core.mail import send_mail,EmailMessage

def Student_signup(request):
    
    
    return render(request, 'signup.html' )

def do_signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lname')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        gender=request.POST.get('gender')

        print('fkkkkkkkkkkkkkkk',firstname,lastname,email,username,password,gender)
        
        if CustomUser.objects.filter(email = email).exists():
            messages.warning(request, "Email is already Taken")
            return redirect('stdsignup')

        if CustomUser.objects.filter(username = username).exists():
            messages.warning(request, "Username is already Taken")
            return redirect('stdsignup')

        else:
            user = CustomUser(
                first_name = firstname,
                last_name = lastname,
                username = username,
                email = email,
                user_type = 3
            )
            user.set_password(password)
            user.save()
            student = Student(
                admin = user,
                gender = gender,
            )
            student.save()       
            messages.success(request, user.first_name + "  "+ user.last_name + ' Are Successfully Registered !!' )
            return redirect('Home')
           
    return redirect('Home')



def index(request):
     return render(request, 'home.html' )

def LOGIN(request):
    return render(request, 'login.html')

def Videos(request):
    video = Video.objects.all()
    return render(request,'video.html',{'video':video})

def ADDVIDEOS(request):
    if request.method =="POST":
        video_course=request.FILES.getlist('profile_course_pic')
        for vi in video_course:
            vid = Video.objects.create(video=vi)
            
        print(vi)


    return render(request, 'HOD/add_videos.html')

def Home(request):
    
    # catgry1 = category.objects.all()[0]
    # catgry = category.objects.all()[1]
    catgry = category.objects.all()
    categoryID = request.GET.get('category')
    # categoryID = request.objects.GET.get('category')
    if categoryID:
        course = Course.objects.filter(couse_category=categoryID)
        
    else:
        course = Course.objects.all()
       
    # print(catgry1,catgry)
    # Location.objects.all()[0]
    # print(course)
    context ={
        'course':course,
        'category':catgry
    }
    
    return render(request, 'Homepage/home.html',context)

def courses(request):
    return render(request, 'Homepage/courses.html')

def aboutus(request):
    return render(request, 'Homepage/aboutus.html')

def contactus(request): 
    if request.method == "POST":
        rec = request.POST.get('to')
        sub = request.POST.get('sub')
        msg = request.POST.get('message')
        try:
            em = EmailMessage(sub,msg,to=[rec,])
            em.send()
            
        except:
            pass


    return render(request, 'Homepage/contactus.html')
     # if request.method =='POST':
    #     first_name= request.POST['first_name']
    #     email_address=request.POST['email_address']
    #     message=request.POST['message']
    #     print("dddddddddddddddddddddddddddfffffffffffff",first_name,email_address,message)
    #     send_mail('contact Form', first_name, email_address,message,
    #               settings.EMAIL_HOST_USER,
    #               ['tarunsharma991723@gmail.com'],
    #               fail_silently=False)
    # return render(request, 'Homepage/contactus.html')
    
    
#    if request.method == 'POST':
#        first_name = request.POST.get('first_name')
#        email_address = request.POST.get('email_address')
#        message = request.POST.get('message')

#        send_mail(
#          first_name, # subject
#          email_address, [email_address],
#          message, # message
#          ['armaan@1994@gmail.com'],
           
#        )
#        return render(request, 'Homepage/contactus.html')
#    else:
#      return render(request, 'Homepage/contactus.html')



def Add_To_Cart(request):
    return render(request, 'Homepage/addtocart.html')

def PLACEORDER(request):
    if request.method =="POST":
        username = request.POST.get('username')
        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')
        # print("dddddddddddddddddddd",username)
        # print("orderrrrrrrrrrrrrrr", order_id)
        # print("paymentttttttttttttt", payment)
    return render(request, 'placeorder.html')

def CourseDetail(request,pk):
   if request.method=='POST':
     course=Course.objects.all().filter(course_id=pk)
   else:
     course=Course.objects.all().filter(course_id=pk)
     pic= CustomUser.objects.filter(staff=pk)
   return render(request, 'Homepage/course-detail.html',{'course':course , 'pic':pic})

def right(request,id):
   
    
    course = Course.objects.filter(pk=id)
    course1 = Course.objects.filter(course_id=id)
    
        # return redirect('right')
    # def  Buy_Course(request , id):
    # current_user = request.user
    # amount = current_user.amount
    # ll = request.POST.get('total')
    # print("ddddddddddddddddd",ll)
    # payment = client.order.create({
    #     "amount": 500,
    #     "currency": "INR",
    #     "payment_capture" :"1"
    # })
    # order_id = payment['id']
    
    # print("paymenttttttttttttttttt",payment)
    # print("orderrrrrrrrrrrrrrrrrrrrrrrrr",order_id)
    
    # print(course)
    context = {
        'course':course,
        'course1':course1
        
    }

   
    
    return render(request, 'Homepage/rightsidebar.html',context)

#    if request.method=='POST':
#      course=Course.objects.all().filter(course_id=pk)
#    else:
#      course=Course.objects.all().filter(course_id=pk)
#      pic= CustomUser.objects.filter(staff=pk)
#    return render(request, 'Homepage/course-detail.html',{'course':course , 'pic':pic})

#####Right page####
# def right(request,pk):
#    if request.method=='POST':
#        course=Course.objects.all().filter(course_id=pk)
#    else:
#        course=Course.objects.all().filter(course_id=pk)
#        pic= CustomUser.objects.filter(staff=pk)
#    return render(request, 'Homepage/rightsidebar.html',{'aaa':course , 'pic':pic})



# def pk_Instructor(request , id):
#     if request.method=="POST":
#         pic=request.POST.get(id=id)
#     else:    
#         pic=Staff.objects.all().filter(id=pic)
#         return render(request, 'Homepage/course-detail.html' , {})

    
@login_required(login_url='doLogin')
def  Buy_Course(request , id):
    course1=Course.objects.all().filter(course_id=id)
    course = Course.objects.filter(pk=id)
    # amount = request.post.get('amount')
     
    context ={
    'course':course,
    # 'payment':payment,
    # 'order_id':order_id,
    'course1':course1,
    
    
}
    if request.method == "POST":
        course1=Course.objects.all().filter(course_id=id)
        course = Course.objects.filter(pk=id)

        uid = request.session.get('_auth_user_id')
        user = CustomUser.objects.get(id=uid)
        name = request.POST.get("name")
        # print("nameeeeeeeeeeee",name)
        amount2 = int(request.POST.get("amount")) 
        amount =amount2*100
        # print("amountttttttttttttttttttttttt",amount)
        client=razorpay.Client(auth =("rzp_live_i4OVIpsxBoHieZ" , "tWbWS8vpbMSFzcXyadmk5YVT"))
        payment=client.order.create({'amount':amount, 'currency':'INR' , 'payment_capture' : '1'})
        coffee=order(name = name , amount = amount2 , payment_id = payment['id'],user=user)
        coffee.save()
        # return HttpResponseRedirect(reverse("Home"))
         
        context ={
        'course':course,
        # 'payment':payment,
        # 'order_id':order_id,
        'course1':course1,
        'payment':payment
        
        
    }
        return render(request , 'Homepage/checkout.html', context)
        
    return render(request, 'Homepage/checkout.html',context)

    # current_user = request.user
    # print(current_user)
    
    # amount = current_user.amount
    
    
    # print("paymenttttttttttttttttt",payment)
    # print("orderrrrrrrrrrrrrrrrrrrrrrrrr",order_id)
    
    # print(course)

    # if request.method =="POST":
    #     uid = request.session.get('_auth_user_id')
    #     user = CustomUser.objects.get(id=uid)
    #     # print("userrrrrrrrrrrrr",user)
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     mob = request.POST.get('mob')
    #     country = request.POST.get('country')
    #     state = request.POST.get('state')
    #     pin = request.POST.get('pin')
    #     address = request.POST.get('address')
    #     total = request.POST.get('total')
    #     # print(total)


    #     order_id = request.POST.get('order_id')
    #     payment = request.POST.get('payment')

    #     odr = order(
    #         user = user,
    #         name = username,
    #         email = email,
    #         mobile = mob,
    #         country = country,
    #         state = state,
    #         postal_code = pin,
    #         address = address,
    #         payment_id = order_id,
    #         amount = total
    #     )
    #     odr.save()

    #     # print("helooooooooooo",username,email,mob,country,state,pin,address,order_id,payment)
    # ll = request.POST.get('amount')
    # print("ddddddddddddddddd",ll)
    # payment = client.order.create({
    #     "amount": 200,
    #     "currency": "INR",
    #     "payment_capture" :"1"
    # })
    # order_id = payment['id']
   
    
    
    # return render(request, 'Homepage/checkout.html',context)


@csrf_exempt
def success(request):
    if request.method=="POST":
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
        user = order.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
        
    return render(request,'thankyou.html')

@csrf_exempt
def doLogin(request):
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, 
                                        username = request.POST.get('email'),
                                        password=request.POST.get('password'),)
        if user!=None:
            login(request,user)                                        
            user_type = user.user_type
            if user_type == '1':
                return redirect("hod_home")
               
            elif user_type == '2':
                return redirect("Instructor_Dashboard")
            elif user_type =='3':
                return redirect('Student_dashboard')
                # return HttpResponse("This is Student Panel")
            else:
                messages.error(request, "Email or Passwrod are Invalid !!")
                return redirect('LOGIN')
        else:
            return redirect('LOGIN')
    else:
            return redirect('LOGIN')


def doLogout(request):
    logout(request)
    return redirect('Home')
