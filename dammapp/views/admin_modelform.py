from django import forms

from dammapp import models
from dammapp.utils.encrypt import md5


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name,field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = "form-control"
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {"class": "form-control", 'placeholder': field.label}


class AdminModelForm(BootstrapModelForm):
    class Meta:
        model = models.Admin
        exclude = []

    def clean_name(self):
        txt_name = self.cleaned_data['name']
        exists = models.Admin.objects.filter(name=txt_name).exists()
        if exists:
            raise forms.ValidationError('该用户名已存在')
        return txt_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        pwd = md5(pwd)
        return pwd


class WorkTypeModelForm(BootstrapModelForm):
    class Meta:
        model = models.WorkType
        exclude = ['typeId']
    
    def clean_typeName(self):
        txt_typeName = self.cleaned_data['typeName']
        exists = models.WorkType.objects.filter(typeName=txt_typeName).exists()
        if exists:
            raise forms.ValidationError('该工种已存在')
        return txt_typeName


class MaintenanceItemModelForm(BootstrapModelForm):
    class Meta:
        model = models.MaintenanceItem
        exclude = ['itemId']

    def clean_itemName(self):
        txt_itemName = self.cleaned_data['itemName']
        exists = models.MaintenanceItem.objects.filter(itemName=txt_itemName).exists()
        if exists:
            raise forms.ValidationError('该维修项目已存在')
        return txt_itemName


class PartsModelForm(BootstrapModelForm):
    class Meta:
        model = models.Parts
        fields = '__all__'


class CustomerModelForm(BootstrapModelForm):
    class Meta:
        model = models.Customer
        exclude = ['uid']


class CustomerCarModelForm(BootstrapModelForm):
    class Meta:
        model = models.CustomerCar
        fields = '__all__'


class SalesmanModelForm(BootstrapModelForm):
    class Meta:
        model = models.Salesman
        # fields = '__all__'
        exclude = ['sid']


class MaintenanceManModelForm(BootstrapModelForm):
    class Meta:
        model = models.MaintenanceMan
        # fields = '__all__'
        exclude = ['mid']


class MaintenanceOrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.MaintenanceOrder
        # fields = '__all__'
        exclude = ['orderId']


class MaintenanceWorkOrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.MaintenanceWorkOrder
        # fields = '__all__'
        exclude = ['workOrderId']


class UsePartsModelForm(BootstrapModelForm):
    class Meta:
        model = models.UseParts
        # fields = '__all__'
        exclude = ['nId']
