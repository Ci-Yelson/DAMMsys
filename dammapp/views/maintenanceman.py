from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone

from dammapp import models


#=================== ModelForm ===================

class MaintenanceManInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.MaintenanceMan
        # fields = '__all__'
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled": "true"}

class WorkOrderInfoModelForm(forms.ModelForm):
    vin = forms.CharField(label='车架号', max_length=17)
    faultDiscribe = forms.CharField(label='故障描述')

    class Meta:
        model = models.MaintenanceWorkOrder
        # fields = '__all__'
        exclude = ['workOrderId', 'orderId', 'sid', 
                    'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == "mid":
                field.label = "维修员(ID-姓名)"
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label, "disabled": "true"}


class UsePartModelForm(forms.ModelForm):
    class Meta:
        model = models.UseParts
        # fields = '__all__'
        exclude = ['workOrderId', 'partCost']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            # print(name, field)
            if name == 'partId':
                field.label = '零件名称'
            field.widget.attrs = {"class": "form-control", 'placeholder': field.label}
    

#=================== ModelForm ===================


def maintenanceman_home(request):

    mid = request.session['info']['userid']
    obj = models.MaintenanceMan.objects.filter(mid=mid).first()
    formInfo = MaintenanceManInfoModelForm(instance=obj)

    # 【待开始】
    workOrderList_1 = models.MaintenanceWorkOrder.objects.filter(mid=obj, status=1).all()
    # 【进行中】
    workOrderList_2 = models.MaintenanceWorkOrder.objects.filter(mid=obj, status=2).all()
    # 【已完成】
    workOrderList_3 = models.MaintenanceWorkOrder.objects.filter(mid=obj, status=3).all()

    # print(">>>", "workOrderList_1: ", workOrderList_1)

    ctx = {'formInfo': formInfo, 
            'workOrderList_1': workOrderList_1, 'workOrderList_2': workOrderList_2, 'workOrderList_3': workOrderList_3}
    return render(request, 'maintenanceman/home.html', context=ctx)


def workorder_detail(request):

    workOrderId = request.GET.get('workOrderId')
    print(">>>", 'workOrderId: ', workOrderId)
    obj = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()
    workOrderStatus = obj.get_status_display()
    
    workOrderInfoForm = WorkOrderInfoModelForm(instance=obj)
    workOrderInfoForm.data['vin'] = obj.orderId.vin
    workOrderInfoForm.instance.faultDiscribe = obj.orderId.faultDiscribe

    for name, field in workOrderInfoForm.fields.items():
        if name == "vin":
            field.widget.attrs['value'] = obj.orderId.vin
        if name == "faultDiscribe":
            field.widget.attrs['value'] = obj.orderId.faultDiscribe

    if workOrderStatus == "待开始":
        workOrderInfoForm.fields.pop('artificialCost')
        workOrderInfoForm.fields.pop('totalPartsCost')
    if workOrderStatus == "进行中":
        workOrderInfoForm.fields.pop('artificialCost')

    usePartList = []
    addUsePartForm = None
    if workOrderStatus != "待开始":
        usePartList = models.UseParts.objects.filter(workOrderId=workOrderId).all()
        addUsePartForm = UsePartModelForm()

    ctx = {'workOrderId': workOrderId, 'workOrderStatus': workOrderStatus, 
            'workOrderInfoForm': workOrderInfoForm, 'usePartList': usePartList, 
            'addUsePartForm': addUsePartForm}
    return render(request, 'maintenanceman/workorder_detail.html', context=ctx)


def start_workorder(request):

    # 状态检测 - 保证维修员只能有一项任务处于“进行中“状态
    obj_mm = models.MaintenanceMan.objects.filter(mid=request.session['info']['userid']).first()
    if obj_mm.status == 2:
        return HttpResponse("Error: 当前维修员已在工作中，不能再开始新的任务。")
    

    workOrderId = request.GET.get('workOrderId')
    print(">>>", 'start_workorder workOrderId: ', workOrderId)
    obj = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()
    workOrderStatus = obj.status
    if workOrderStatus != 1:
        return HttpResponse("Error: 派工单状态错误")
    
    upd_data = dict()
    upd_data['status'] = 2
    upd_data['startTime'] = timezone.now()
    models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).update(**upd_data)
    #todo 触发器实现
    # models.MaintenanceMan.objects.filter(mid=request.session['info']['userid']).update(status=2)
    #todo 触发器实现
    
    return redirect('/maintenanceman/workorder_detail/?workOrderId='+workOrderId)


def finish_workorder(request):

    workOrderId = request.GET.get('workOrderId')
    print(">>>", 'finish_workorder workOrderId: ', workOrderId)
    obj = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()
    orderId = obj.orderId.orderId
    workOrderStatus = obj.status
    if workOrderStatus != 2:
        return HttpResponse("Error: 派工单状态错误")
    
    upd_data = dict()
    upd_data['status'] = 3
    upd_data['endTime'] = timezone.now()
    # 实际工时 - 上取整
    upd_data['hour'] = ((upd_data['endTime'] - obj.startTime).seconds + 3599) / 3600
    upd_data['artificialCost'] = upd_data['hour'] * obj.mid.workType.price

    models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).update(**upd_data)
    #todo 触发器实现
    # obj_order = models.MaintenanceOrder.objects.filter(orderId=orderId).first()
    # order_cost = obj_order.cost
    # order_cost += upd_data['artificialCost'] + obj.totalPartsCost
    # models.MaintenanceOrder.objects.filter(orderId=orderId).update(cost=order_cost)
    # models.MaintenanceMan.objects.filter(mid=request.session['info']['userid']).update(status=1)
    #todo 触发器实现

    return redirect('/maintenanceman/workorder_detail/?workOrderId='+workOrderId)


@csrf_exempt
def add_usepart(request):

    workOrderId = request.GET.get('workOrderId')
    print(">>>", 'add_usepart workOrderId: ', workOrderId)
    obj_workOrder = models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).first()
    usePartForm = UsePartModelForm(data=request.POST)

    # 状态检测
    if obj_workOrder.status != 2:
        return JsonResponse({'status': False, 'error': 'workOrder status error.'})

    if usePartForm.is_valid():
        usePartForm.instance.workOrderId = obj_workOrder
        _price = usePartForm.instance.partId.price
        _num = usePartForm.instance.partNumber
        usePartForm.instance.partCost = _num * _price

        usePartForm.save()

        #todo 触发器实现
        # _totalPartsCost = 0
        # if obj_workOrder.totalPartsCost:
        #     _totalPartsCost = obj_workOrder.totalPartsCost
        # _totalPartsCost += usePartForm.instance.partCost
        # models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).update(totalPartsCost=_totalPartsCost)
        #todo 触发器实现

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': usePartForm.errors})


@csrf_exempt
def del_usepart(request):

    nId = request.GET.get('nId')
    #todo 触发器实现
    # obj_up = models.UseParts.objects.filter(nId=nId).first()
    # obj_workOrder = obj_up.workOrderId
    # # 状态检测
    # if obj_workOrder.status != 2:
    #     return JsonResponse({'status': False, 'error': 'workOrder status error.'})
    # _partCost = obj_up.partCost
    # _totalPartsCost = obj_workOrder.totalPartsCost
    # _totalPartsCost -= _partCost
    # models.MaintenanceWorkOrder.objects.filter(workOrderId=obj_workOrder.workOrderId).update(totalPartsCost=_totalPartsCost)
    #todo 触发器实现
    models.UseParts.objects.filter(nId=nId).delete()

    return JsonResponse({'status': True})