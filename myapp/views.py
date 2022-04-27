from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse,FileResponse
import datetime
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

def login(request):
    if request.session.has_key('is_login'):
        return redirect('home')
    if request.POST:
        userEmail = request.POST['userEmail']
        userPassword = request.POST['userPassword']
        count = User.objects.filter(userEmail=userEmail, userPassword=userPassword).count()
        if count > 0:
            request.session['is_login'] = True
            request.session['user_id'] = \
            User.objects.values('id').filter(userEmail=userEmail, userPassword=userPassword)[0]['id']
            return redirect('home')
        else:
            messages.error(request, "Wrong Id or Password")
            return redirect('login')

    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def registerUser(request):
    if request.POST:
        userName = request.POST['userName']
        userEmail = request.POST['userEmail']
        userPassword = request.POST['userPassword']
        obj = User(userName=userName, userEmail=userEmail, userPassword=userPassword)
        obj.save()
        messages.success(request, "Signup Succesful")
        return redirect('login')


def home(request):
    if request.session.has_key('is_login'):
        data = Blog.objects.all
        return render(request, 'home.html', {'data': data})


def logout(request):
    del request.session['is_login']
    return redirect('login')


def createPost(request):
    if request.POST:
        image = request.FILES['image']
        title = request.POST['title']
        postDetail = request.POST['postDetail']
        publisherName = request.POST['publisherName']
        user_id = request.POST['user_id']
        obj = Blog(image=image, title=title, postDetail=postDetail, publisherName=publisherName)
        obj.user_id_id = user_id
        obj.save()
    return render(request, 'createPost.html')


def readMore(request, id):
    if request.POST:
        messages = request.POST['messages']
        user_id = request.POST['user_id']
        post_id = id
        query = Comment(messages=messages)
        query.user_id_id = user_id
        query.post_id_id= post_id
        query.save()
    data = Blog.objects.get(id=id)
    comment = Comment.objects.all().filter(post_id=id)
    return render(request, 'readMore.html', {'data': data,'comment':comment})

def demo(request):
    return render(request,'dmeo.html')

# class FirstMiddleware:
#     def __init__(self,get_response):
#         self.get_response = get_response
#
#     def __call__(self,request):
#         response = self.get_response(request)
#         return response

def export_csv(request):
    response = HttpResponse(content_type='txt/csv')
    response['Content-Disposition']='attachment; filename=Hitesh' + str(datetime.datetime.now())+'.csv'
    fieldNames = ['Name','Email']
    writer = csv.DictWriter(response,fieldNames)
    writer.writeheader()
    writer.writerow({'Name':'Hitesh','Email':'hitesh@gmail.com'})
    return response

def export_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    txtobj = c.beginText()
    txtobj.setTextOrigin(inch,inch)

    lines = [
        "This is my first Line\n"
        "This is my Second Line\n"
        "This is my Third Line\n"
    ]
    for line in lines:
        txtobj.textLine(line)

    c.drawText(txtobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename=str(datetime.datetime.now())+'.pdf')