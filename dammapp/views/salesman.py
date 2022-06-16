from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from dammapp import models


#=================== ModelForm ===================

class SalesmanInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.Salesman
        # fields = '__all__'
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled": "true"}


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceOrder
        # fields = '__all__'
        exclude = ['sid', 'status', 'sName', 'phone']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == 'finishDatetime':
                field.widget = forms.DateInput(attrs={"class": "form-control", 'placeholder': field.label, "disabled": "true", 'type':'date'})
            else:
                field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled": "true"}


class EditOrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceOrder
        # fields = '__all__'
        fields = ['finishDatetime', 'cost']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == 'finishDatetime':
                field.widget = forms.DateInput(attrs={"class": "form-control", 'placeholder': field.label, 'type':'date'})
            else:
                field.widget.attrs = {"class": "form-control", 'placeholder': field.label} 


class WorkOrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceWorkOrder
        # fields = '__all__'
        exclude = ['workOrderId', 'orderId', 'sid', 
                    'status', 'artificialCost', 'totalPartsCost',
                    'startTime', 'endTime']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == "mid":
                field.label = "维修员(ID-姓名)"
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}


class WorkOrderDetailModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceWorkOrder
        # fields = '__all__'
        exclude = ['workOrderId', 'orderId', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == "mid":
                field.label = "维修员(ID-姓名)"
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled": "true"} 


class EditWorkOrderModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceWorkOrder
        # fields = '__all__'
        exclude = ['workOrderId', 'orderId', 'status', 'startTime', 'endTime']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == "mid":
                field.label = "维修员(ID-姓名)"
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label} 

#=================== ModelForm ===================


def salesman_home(request):

    sid = request.session['info']['userid']
    obj = models.Salesman.objects.filter(sid=sid).first()
    formInfo = SalesmanInfoModelForm(instance=obj)

    # 【待受理】委托
    orderList_1 = models.MaintenanceOrder.objects.filter(status=1).all()
    # 【正在维修】委托
    orderList_2 = models.MaintenanceOrder.objects.filter(sid=obj, status=2).all()
    # 【已完成维修】委托
    orderList_3 = models.MaintenanceOrder.objects.filter(sid=obj, status=3).all()

    ctx = {'formInfo': formInfo, 'orderList_1': orderList_1, 'orderList_2': orderList_2, 'orderList_3': orderList_3}

    return render(request, 'salesman/home.html', context=ctx)


def order_detail(request):

    orderId = request.GET.get('orderId')
    obj = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
    orderStatus = obj.get_status_display()
    orderInfoForm = OrderModelForm(instance=obj)
    orderEditForm = EditOrderModelForm(instance=obj)

    workOrderList = models.MaintenanceWorkOrder.objects.filter(orderId=orderId).all()
    workOrderForm = WorkOrderModelForm()

    ctx = {'orderId': orderId, 'orderStatus': orderStatus, 'orderInfo': orderInfoForm, 'orderEditForm': orderEditForm, 'workOrderList': workOrderList, 'workOrderForm': workOrderForm}
    return render(request, 'salesman/order_detail.html', context=ctx)


def accept_order(request):

    orderId = request.GET.get('orderId')
    # print(">>>", 'orderId', orderId)
    obj_order = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
    order_status = obj_order.status
    if order_status != 1:
        return HttpResponse('Erorr: 委托单状态错误')

    sid = request.session['info']['userid']
    # print(">>>", 'sid', sid)
    obj_salesman = models.Salesman.objects.filter(sid=sid).first()

    upd_data = {'sid': obj_salesman, 
                'sName': obj_salesman.sName, 
                'phone': obj_salesman.phone, 
                'status': 2,
                'cost': 0,}
    models.MaintenanceOrder.objects.filter(orderId=orderId).update(**upd_data)
    
    return redirect('/salesman/order_detail/?orderId='+orderId)


def finish_order(request):
    '''完成委托'''
    orderId = request.GET.get('orderId')
    print(">>>", "finish_order orderId: ", orderId)

    obj_order = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
    order_status = obj_order.status
    vin = obj_order.vin.vin
    if order_status != 2:
        return HttpResponse('Erorr: 委托单状态错误')
    
    exists_1 = models.MaintenanceWorkOrder.objects.filter(orderId=obj_order, status=1).exists()
    exists_2 = models.MaintenanceWorkOrder.objects.filter(orderId=obj_order, status=2).exists()
    if exists_1 or exists_2:
        return HttpResponse('Erorr: 当前委托存在未完成的维修项目')
    
    models.MaintenanceOrder.objects.filter(orderId=orderId).update(status=3)
    # todo更新状态 - 客户车辆状态
    # models.CustomerCar.objects.filter(vin=vin).update(status=1)

    return redirect('/salesman/order_detail/?orderId='+orderId)


@csrf_exempt
def edit_order(request):
    '''编辑委托信息'''
    orderId = request.GET.get('orderId')
    print(">>>", "orderId: ", orderId)

    orderEditForm = EditOrderModelForm(data=request.POST)
    if orderEditForm.is_valid():
        upd_data = dict()
        upd_data['finishDatetime'] = orderEditForm.instance.finishDatetime
        upd_data['cost'] = orderEditForm.instance.cost
        models.MaintenanceOrder.objects.filter(orderId=orderId).update(**upd_data)

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': orderEditForm.errors})


@csrf_exempt
def add_workorder(request):
    sid = request.session['info']['userid']
    obj_salesman = models.Salesman.objects.filter(sid=sid).first()
    orderId = request.GET.get('orderId')
    obj_orderId = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
    form = WorkOrderModelForm(data=request.POST)

    if form.is_valid():
        # print(">>>", form.cleaned_data)
        form.instance.status = 1
        form.instance.orderId = obj_orderId
        form.instance.sid = obj_salesman
        form.instance.artificialCost = 0
        form.instance.totalPartsCost = 0
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def workorder_detail(request):

    workOrderId = request.GET.get('workOrderId')
    print(">>>", "workOrderId: ", workOrderId)
    obj = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()
    workOrderStatus = obj.get_status_display()
    workOrderInfoForm = WorkOrderDetailModelForm(instance=obj)
    workOrderEditForm = EditWorkOrderModelForm(instance=obj)

    usePartsList = models.UseParts.objects.filter(workOrderId=workOrderId).all()

    ctx = {'workOrderId': workOrderId, 'workOrderStatus': workOrderStatus, 
            'workOrderInfoForm': workOrderInfoForm, 'workOrderEditForm': workOrderEditForm, 
            'usePartsList': usePartsList}
    return render(request, 'salesman/workorder_detail.html', context=ctx)
    

@csrf_exempt
def edit_workorder(request):

    workOrderId = request.GET.get('workOrderId')
    print(">>>", "workOrderId: ", workOrderId)
    obj = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()

    workOrderEditForm = EditWorkOrderModelForm(data=request.POST, instance=obj)
    if workOrderEditForm.is_valid():
        
        workOrderEditForm.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': workOrderEditForm.errors})