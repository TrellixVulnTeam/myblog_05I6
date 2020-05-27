from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def user_login(request):
    if request.method=='POST':
        user_login_form=UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data=user_login_form.cleaned_data
            user=authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect('article:article_list_article_urls')
            else:
                message='Incorrect username or password.'
                context={'message':message}
                return render(request,'userprofile/login.html',context)
        else:
            message = 'Invalid input.'
            context = {'message': message}
            return render(request, 'userprofile/login.html', context)
    elif request.method=='GET':
        user_login_form=UserLoginForm()
        context={ 'form':user_login_form}
        return render(request,'userprofile/login.html',context)
    else:
        message = 'Pls use POST or GET.'
        context = {'message': message}
        return render(request, 'userprofile/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('article:article_list_article_urls')

def user_register(request):
    if request.method=='POST':
        user_register_form=UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            password=user_register_form.cleaned_data['password']
            password2=user_register_form.cleaned_data['password2']
            if password==password2:
                new_user=user_register_form.save(commit=False)
                new_user.set_password(user_register_form.cleaned_data['password'])
                new_user.save()
                login(request,new_user)
                return redirect('article:article_list_article_urls')
            else:
                message = 'Password not match.'
                context = {'message': message}
                return render(request, 'userprofile/register.html', context)
        else:
            message = 'Invalid input.'
            context = {'message': message}
            return render(request, 'userprofile/register.html', context)
    elif request.method=='GET':
        user_register_form=UserRegisterForm()
        context={ 'form':user_register_form}
        return render(request,'userprofile/register.html',context)
    else:
        message = 'Pls use POST or GET.'
        context = {'message': message}
        return render(request, 'userprofile/register.html', context)

@login_required(login_url='/userprofile/login/')
def user_delete(request,id_user_delete):
    if request.method=='POST':
        user=User.objects.get(id=id_user_delete)
        if request.user==user:
            logout(request)
            user.delete()
            return redirect('article:article_list_article_urls')
        else:
            message = 'You do not have permission.'
            context = {'message': message}
            return render(request, 'article/list.html', context)
    else:
        message = 'Pls use POST.'
        context = {'message': message}
        return render(request, 'article/list.html', context)


