from django.http import FileResponse, Http404
import os
from django.shortcuts import render, redirect
from django.templatetags.static import static
import requests
from .models import *
from django.contrib import messages
import bcrypt


# # Create your views here.
# def index(request):
   

#     return render(request,"index.html",context)


#     from django.shortcuts import render, HttpResponse



# Create your views here.
def pdf(request):
    module_dir = os.path.dirname(__file__) 
    file_path = os.path.join(module_dir, 'static/resume.pdf')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
def index(request):
    # try:
    response = requests.get('https://zenquotes.io/api/random/')
    data = response.json()
    context ={
        "quote": data[0]['q'],
        "author":data[0]['a']
    }
    
    return render(request, 'index.html', context)

def dashboard(request):

    return render(request, 'dashboard.html')

def show(request):
    return render(request, 'register_login.html')

def comment(request):
    logged_user = Users.objects.get(id=request.session['login_id'])
    comment=Comments.objects.create(comment=request.POST['comment'],upload_by=logged_user)
    return redirect('/logout')

def logout(request):
    request.session.flush()
    return redirect('/')

def myeyes(request):
    myview=Comments.objects.all()
    context={
        "notes": myview 
    }
    return render(request,'myeyes.html',context)

def aboutme(request):
    return render(request,'aboutme.html')

def login(request):
    errors = Users.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/show_reg_login')
    else:
        users = Users.objects.filter(email=request.POST['email'])
        if users:
            #try to login
            logged_user = users[0]
            password=request.POST['password']
            print(password.encode())
            print(logged_user.password.encode())
            if bcrypt.checkpw(password.encode(),  logged_user.password.encode()):
                request.session['login_id']=logged_user.id
                messages.success(request, "Successfully logged in")
            else: 
                messages.error(request, "Wrong email/password combination")
        else:
            messages.error(request, "Account with email not found")
            # redirect to a success route
        return redirect('/dashboard')

def register(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    print(request.POST['confrim_pw'], "test")
    errors = Users.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/show_reg_login')
    else:
        password=request.POST['password']
        hash_PW= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(password)
        print(hash_PW)
        new_user=Users.objects.create(
            fname=request.POST['fname'], 
            lname=request.POST['lname'],
            email=request.POST['email'],
            password=hash_PW 
        )
        request.session['login_id']=new_user.id
        messages.success(request, "Successfully registered")
        # redirect to a success route
        return redirect('/dashboard')
    return render(request,'register_login.html')
    
        
    
    
