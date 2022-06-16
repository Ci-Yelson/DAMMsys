from django.shortcuts import render, redirect
from django import forms

from dammapp import models
from dammapp.utils.encrypt import md5

#===========LoginForm===========

class LoginForm(forms.Form):
    name = forms.CharField(label='用户名')
    ident = forms.CharField(label='身份')
    password = forms.CharField(label='密码')

    def clean_password(self):
        pwd = self.cleaned_data['password']
        pwd = md5(pwd)
        return pwd
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}


#===============Login/Logout===============

def account_login(request):
    ''' Login '''
    
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        print('>>>', form.cleaned_data)

        ident = form.cleaned_data['ident']
        print('>>>ident:',ident)

        if ident == '客户':
            # 客户登录 - 【用户名 + 密码】
            info = {
                'customerName':form.cleaned_data['name'],
                'password':form.cleaned_data['password'],
            }
            obj = models.Customer.objects.filter(**info).first()
        elif ident == '业务员':
            # 业务员登录 - 【手机号 + 密码】
            info = {
                'phone':form.cleaned_data['name'],
                'password':form.cleaned_data['password'],
            }
            obj = models.Salesman.objects.filter(**info).first()
        elif ident == '维修员':
            # 维修员登录 - 【手机号 + 密码】
            info = {
                'phone':form.cleaned_data['name'],
                'password':form.cleaned_data['password'],
            }
            obj = models.MaintenanceMan.objects.filter(**info).first()
        elif ident == '管理员':
            # 管理员登录 - 【用户名 + 密码】
            info = {
                'name':form.cleaned_data['name'],
                'password':form.cleaned_data['password'],
            }
            obj = models.Admin.objects.filter(**info).first()

        # 登录校验
        if not obj:
            #* 主动添加校验错误
            form.add_error('password','用户名或密码错误')
            return render(request, 'login.html', {'form': form})

        # 校验成功
        if ident == '客户':
            uid = obj.uid
        elif ident == '业务员':
            uid = obj.sid
        elif ident == '维修员':
            uid = obj.mid
        elif ident == '管理员':
            uid = obj.aid

        # 服务端生成随机字符串，并写入客户端浏览器的cookie中，再写入到（数据库中的）session中。
        # ! session['info']存放 username 和 userid
        request.session['info'] = {'username':form.cleaned_data['name'], 'userid':uid}

        print(">>>", "request.session['info']:", request.session['info'])

        if ident == '客户':
            return redirect('/customer')
        elif ident == '业务员':
            return redirect('/salesman')
        elif ident == '维修员':
            return redirect('/maintenanceman')
        elif ident == '管理员':
            return redirect('/admin')

    return render(request, 'login.html', {'form': form})


def account_logout(request):
    ''' Logout '''
    request.session.clear()
    return redirect('/login/')


#===========CustomerRegister===========


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        # fields = '__all__'
        exclude = ['uid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}

    def clean_customerName(self):
        txt_customerName = self.cleaned_data['customerName']
        exists = models.Customer.objects.filter(customerName=txt_customerName).exists()
        print(">>>", exists)
        if exists:
            raise forms.ValidationError('该用户名已注册')
        return txt_customerName

    def clean_password(self):
        pwd = self.cleaned_data['password']
        pwd = md5(pwd)
        return pwd
    

def account_register(request):
    ''' Customer Register '''
    if request.method == 'GET':
        form = CustomerModelForm()
        print(">>>", "register get")
        return render(request, 'register.html', {'form': form})

    form = CustomerModelForm(data=request.POST)
    print(">>>", form.is_valid())
    if form.is_valid():
        print('>>>', form.cleaned_data)

        # 插入新数据并自动登录
        form.save()
        uid = models.Customer.objects.filter(customerName=form.cleaned_data['customerName']).first().uid

        # 服务端生成随机字符串，并写入客户端浏览器的cookie中，再写入到（数据库中的）session中。
        request.session['info'] = {'username':form.cleaned_data['customerName'], 'userid':uid}

        print(">>>", "request.session['info']:", request.session['info'])
        return redirect('/customer')
    else:
        print(">>>", form.errors)
        return render(request, 'register.html', {'form': form})