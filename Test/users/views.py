from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .models import UserProfile  # 一对一用户信息表
from django.contrib import auth 
from .forms import RegistrationForm, LoginForm, ProfileForm, PwdChangeForm  # 导入定义好的表单
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required # 登录装饰器
from django.utils import timezone

# 注册
def register(request):
    # 只有当使用request的方法是post请求数据时才可以
    if request.method == "POST":
        # request.POST获取POST请求参数，然后实例化一个类，
        form = RegistrationForm(request.POST)
        # 验证form里的数据是否有效
        if form.is_valid():
            '''
            # form.cleaned_data读取表单返回的值
            # form.cleaned_data返回类型为字典dict型
            '''
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # 将验证通过的数据存入数据库，create_user已经自动哈希加密
            user = User.objects.create_user(username=username, password=password, email=email)
            # 这里的user是一个model
            UserProfile.objects.create(user=user) # 用户和用户的信息一对一关系，OneToOne
            return HttpResponseRedirect('/accounts/login/') # 注册成功后重定向到登录界面
    else:
        form = RegistrationForm() # 生成一个空的表单
    return render(request, 'users/register.html', {'form':form})


# 登录
def login(request):
    # 通过POST方法提交表单
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("users:profile", args=[user.id])) # 反向解析url
            else:
                # 登陆失败
               return render(request, 'users/login.html', {'form': form, 'message': '密码或帐号错误'})
    
    else:
        # 否侧就生成一个空的表格
        form = LoginForm()
    # 如果没有提交表单或不是通过POST方法提交表单、生成一张空的RegistrationForm
    return render(request, 'users/login.html',{'form':form})

# 修改密码
@login_required
def pwd_change(request, pk):
    # 用特定查询条件获取某个对象，成功则返回该对象，否则引发一个 Http404。
    # 查询主键为pk的用户，找不到返回http404
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = PwdChangeForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse("users:profile", args=[user.id])) # 反向解析url
    else:
        form = PwdChangeForm()
    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})


# auth内置的装饰器，只有先登录才能可以操作下面的函数
# 现实用户资料
@login_required
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {"user":user})

'''
# 从url获取user的主键pk(id), 
# get_object_or_404获取需要修改个人资料的用户对象user
# 然后再user获取一一对应的user_profile对象
'''
@login_required
def profile_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # fist_name和last_name是在User表中
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save() # 数据存入
            # org和telep字段是在UserProfile中
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save() # 数据存入
            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:

        default_data = {'first_name': user.first_name, 'last_name': user.last_name, 'org': user_profile.org, 'telephone': user_profile.telephone }
        form = ProfileForm(default_data)
    
    return render(request, 'users/profile_update.html', {'form': form, 'user': user})