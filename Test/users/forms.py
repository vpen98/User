from django import forms
from django.contrib.auth.models import User
import re

# 使用正则表达式验证邮箱的格式，满足返回1，否则返回0
def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)
# 注册表单
class RegistrationForm(forms.Form):
    username = forms.CharField(label='帐号', max_length=50)
    email = forms.EmailField(label="邮箱")
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码(重复)', widget=forms.PasswordInput)
    # 验证输入的帐号是否符合要求
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 6:
            raise forms.ValidationError("帐号需小于6位")
        elif len(username) > 12:
            raise forms.ValidationError("帐号太长")
        else:
            # 验证帐号是否存在
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("帐号已存在")
        return username
    
    # 验证邮箱的
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # 验证邮箱的格式
        if email_check(email):
            # 验证邮箱是否存在
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("邮箱已存在")
        else:
            raise forms.ValidationError("请输入正确的邮箱")
        
        return email
    
    # 验证输入的密码是否符合要求
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("密码要大于8位")
        elif len(password1) > 16:
            raise forms.ValidationError("密码要小于20位")
        return password1
    
    # 两次输入的密码是否一样
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不一样")
        return password2
# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email_check__exact=username)
            if not filter_result:
                raise ValidationError("email 不存在")
            else:
                filter_result = User.objects.filter(username__exact=username)
                if not filter_result:
                    raise forms.ValidationError("This username does not exist. Please register first.")
            
        return username

# 用户信息表单
class ProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=50, required=False)
    last_name = forms.CharField(label='Last Name', max_length=50, required=False)
    org = forms.CharField(label='住址', max_length=50, required=False)
    telephone = forms.CharField(label='电话', max_length=50, required=False)

# 修改密码的表单
class PwdChangeForm(forms.Form):
    password1 = forms.CharField(label='新密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='新密码', widget=forms.PasswordInput)
        
    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("密码要大于8位")
        elif len(password1) > 16:
            raise forms.ValidationError("密码要小于20位")
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不一样")
        return password2