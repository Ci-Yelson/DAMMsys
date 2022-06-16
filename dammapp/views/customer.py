from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django import forms
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime


from dammapp import models

#=================== ModelForm ===================

class CustomerInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        # fields = '__all__'
        exclude = ['uid','password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}

class CustomerCarModelForm(forms.ModelForm):
    class Meta:
        model = models.CustomerCar
        exclude = ['uid', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}

class AddOrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceOrder
        fields = ['maintenanceType', 'category', 'payway', 'inDatetime', 'faultDiscribe', 'oil', 'mileage']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == 'inDatetime':
                field.widget = forms.DateInput(attrs={"class": "form-control", 'placeholder': field.label, 'type':'date'})
            else:
                field.widget.attrs = {"class": "form-control", 'placeholder': field.label} 

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceOrder
        # fields = '__all__'
        exclude = ['sid', 'status', 'customerName', 'vin', 'recordDate', 'customerPhone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled":"true"} 


def customer_home(request):

    customer_name = request.session['info']['username']
    customer_info = models.Customer.objects.filter(customerName=customer_name).first()
    customer_info_form_show = CustomerInfoModelForm(instance=customer_info)
    customer_info_form_edit = CustomerInfoModelForm(instance=customer_info)
    customer_cars_info = models.CustomerCar.objects.filter(uid_id=customer_info.uid).all()

    for name, field in customer_info_form_show.fields.items():
        field.widget.attrs["disabled"] = "true"

    carform = CustomerCarModelForm()
    addOrderform = AddOrderModelForm()

    ctx = {'customerInfoShow': customer_info_form_show, 'customerInfoEdit': customer_info_form_edit, 'customerCarsInfo': customer_cars_info, 'carform': carform, 'addOrderform': addOrderform}

    return render(request, 'customer/home.html', context=ctx)


@csrf_exempt
def edit_info(request):
    customerName = request.POST.get("customerName")
    obj = models.Customer.objects.filter(customerName=customerName).first()
    form = CustomerInfoModelForm(data=request.POST, instance=obj)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def add_car(request):
    form = CustomerCarModelForm(data=request.POST)

    if form.is_valid():
        # print(">>>", form.cleaned_data)
        uid = request.session['info']['userid']
        print(">>>", "add_car uid:", uid)
        form.instance.uid = models.Customer.objects.filter(uid=uid).first()
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


@csrf_exempt
def add_order(request):
    '''申请维修'''
    vin = request.GET.get('vin')
    print(">>>", "add_order vin:",vin)
    obj_car = models.CustomerCar.objects.filter(vin=vin).first()
    if not obj_car:
        return JsonResponse({'status': False, 'error': '数据缺失'}) 
    if obj_car.status != 1:
        return JsonResponse({'status': False, 'error': '车辆状态错误'}) 

    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        print(">>>", "add_order save")
        obj_customer = models.Customer.objects.filter(uid=request.session['info']['userid']).first()
        form.instance.customerName = obj_customer
        form.instance.customerPhone = obj_customer.phone
        form.instance.recordDate = datetime.now().strftime('%Y-%m-%d')
        form.instance.vin = obj_car
        form.save()
        #todo 更新车辆状态【可用触发器实现】
        # obj_car.status = 2
        # obj_car.save()
        #todo 更新车辆状态【可用触发器实现】

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def order_list(request):
    '''委托列表'''
    vin = request.GET.get('vin')
    orderList = models.MaintenanceOrder.objects.filter(vin=vin).all()
    carobj = models.CustomerCar.objects.filter(vin=vin).first()
    carInfo = CustomerCarModelForm(instance=carobj)
    for name, field in carInfo.fields.items():
        # print(name, field)
        if name == "status":
            field.widget.attrs = {"hidden": "true"}
        else:
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled ":"true"}

    print(">>>", 'carInfo', carInfo)
    return render(request, 'customer/order_list.html', {'orderList':orderList, 'carInfo': carInfo})


def order_detail(request):
    '''委托详情'''
    vin = request.GET.get('vin')
    if vin:
        # 通过'/?vin=vin'访问
        print(">>>", "order_detail vin:",vin)
        obj_car = models.CustomerCar.objects.filter(vin=vin).first()
        print(">>>", "order_detail obj_car:",obj_car)
        obj = models.MaintenanceOrder.objects.filter(vin=obj_car, status__in=[1,2]).first()
        print(">>>", "order_detail obj:",obj)
        if not obj:
            return HttpResponse("Error: 数据缺失")
        orderId = obj.orderId
    else:
        # 通过'/?orderId=orderId'访问
        orderId = request.GET.get('orderId')
        print(">>>", "order_detail orderId:",orderId)
        obj = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
        if not obj:
            return HttpResponse("Error: 数据缺失")
        vin = obj.vin

    orderInfo = OrderModelForm(instance=obj)
    orderStatus = obj.get_status_display()
    print(">>>", 'orderStatus', orderStatus)

    workOrderList = []
    if orderStatus != '待受理':
        workOrderList = models.MaintenanceWorkOrder.objects.filter(orderId=orderId).all()

    ctx = {'orderInfo': orderInfo, 'orderStatus': orderStatus,
            'workOrderList': workOrderList}
    return render(request, 'customer/order_detail.html', context=ctx)



    

