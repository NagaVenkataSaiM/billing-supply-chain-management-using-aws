from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from rest_framework import viewsets, parsers
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from .models import DropBox,Files
from .serializers import DropBoxSerializer
from django.core.files.base import ContentFile
from fpdf import FPDF
import requests
from io import StringIO


# Create your views here.
def home(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			# url='http://127.0.0.1:8000/accounts/'
			# client=requests.session()
			# client.get("http://127.0.0.1:8000/login/")
			# if 'csrftoken' in client.cookies:
			# 	csrftoken = client.cookies['csrftoken']
			# else:
			# 	csrftoken = client.cookies['csrf']
			# print(csrftoken)
			# # Django 1.6 and up
			# # older versions
			# file=request.FILES['document']
			# file.seek(0)
			# file_handle = ContentFile(file.read())
			# payload = {'title': request.POST.get('title'),'document':(file.name,file_handle,)}
			# print(file_handle)
			# r = requests.post(url, data=payload, headers={'X-CSRFToken': csrftoken},
			# allow_redirects=False)
			# print(r.json())
			return redirect('generatebill')
		return render(request,"home.html")
	else:
		return redirect('login')
		
def register(request):
	if request.method=='POST':
		username=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		user=User.objects.create_user(username,email, password)
		user.save()
		return redirect('login')
	return render(request,'register.html')

def login_x(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			request.session['username']=username
			return redirect('home')
		else:
			return redirect('login')
	return render(request,'login.html')

def logout_x(request):
	del request.session['username']
	logout(request)
	return redirect('login')


class DropBoxViewset(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	queryset = DropBox.objects.all()
	serializer_class = DropBoxSerializer
	parser_classes = [parsers.MultiPartParser, parsers.FormParser]
	http_method_names = ['get', 'post', 'patch', 'delete']

def generatebill(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			filename=request.POST.get("filename")
			customername=request.POST.get("customername")
			companyname=request.POST.get("companyname")
			billamount=request.POST.get("billamount")
			pdf=FPDF()
			pdf.add_page()
			pdf.set_font("Arial",size=15)
			pdf.cell(200,10,txt="Dear "+customername,ln=1)
			pdf.cell(200,10,txt="Thank you for purchasing at "+companyname+".your bill Amount is "+billamount,ln=2)
			pdf.output(filename+".pdf")
			files=Files()
			files.title=filename
			files.document=""
			files.uploder=companyname
			files.billowner=customername
			files.save()
		return render(request,"generatebill.html")
	else:
		return redirect('login')

def viewbills(request):
	if request.user.is_authenticated:
		try:
			bills=DropBox.objects.filter(username=request.session['username'])
		except:
			bills=[]
		eve={
		"event_d" : bills
		}
		return render(request,'viewbills.html',eve)
	else:
		return redirect('login')