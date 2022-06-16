from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from dammapp import models
from dammapp.views.admin_modelform import *


# =================管理员账号管理=================
def admin_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['name__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_dict)
    form = AdminModelForm()

    return render(request, 'admin/admin_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_admin(request):
    form = AdminModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_admin(request):
    aid = request.GET.get("aid")
    models.Admin.objects.filter(aid=aid).delete()
    return redirect('/admin/')


# =================工种管理=================
def worktype_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['typeName__contains'] = search_data
    queryset = models.WorkType.objects.filter(**data_dict)
    form = WorkTypeModelForm()

    return render(request, 'admin/worktype_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_worktype(request):
    form = WorkTypeModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_worktype(request):
    typeId = request.GET.get("typeId")
    models.WorkType.objects.filter(typeId=typeId).delete()
    return redirect('/admin/worktype/')


# =================维修项目管理=================
def maintenance_item_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['itemName__contains'] = search_data
    queryset = models.MaintenanceItem.objects.filter(**data_dict)
    form = MaintenanceItemModelForm()

    return render(request, 'admin/maintenance_item_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_maintenance_item(request):
    form = MaintenanceItemModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_maintenance_item(request):
    itemId = request.GET.get("itemId")
    models.MaintenanceItem.objects.filter(itemId=itemId).delete()
    return redirect('/admin/maintenance_item/')


# =================库存零件管理=================
def parts_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['partName__contains'] = search_data
    queryset = models.Parts.objects.filter(**data_dict)
    form = PartsModelForm()

    return render(request, 'admin/parts_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_parts(request):
    form = PartsModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_parts(request):
    partId = request.GET.get("partId")
    models.Parts.objects.filter(partId=partId).delete()
    return redirect('/admin/parts/')                    


# =================客户账号管理=================
def customer_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['customerName__contains'] = search_data
    queryset = models.Customer.objects.filter(**data_dict)
    form = CustomerModelForm()

    return render(request, 'admin/customer_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_customer(request):
    form = CustomerModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_customer(request):
    uid = request.GET.get("uid")
    models.Customer.objects.filter(uid=uid).delete()
    return redirect('/admin/customer/')   


# =================客户车辆管理=================
def customer_car_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['lpn__contains'] = search_data
    queryset = models.CustomerCar.objects.filter(**data_dict)
    form = CustomerCarModelForm()

    return render(request, 'admin/customer_car_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_customer_car(request):
    form = CustomerCarModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_customer_car(request):
    vin = request.GET.get("vin")
    models.CustomerCar.objects.filter(vin=vin).delete()
    return redirect('/admin/customer_car/')   


# =================业务员账号管理=================
def salesman_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['sName__contains'] = search_data
    queryset = models.Salesman.objects.filter(**data_dict)
    form = SalesmanModelForm()

    return render(request, 'admin/salesman_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_salesman(request):
    form = SalesmanModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_salesman(request):
    sid = request.GET.get("sid")
    models.Salesman.objects.filter(sid=sid).delete()
    return redirect('/admin/salesman/')   


# =================维修员员账号管理=================
def maintenanceman_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['mName__contains'] = search_data
    queryset = models.MaintenanceMan.objects.filter(**data_dict)
    form = MaintenanceManModelForm()

    return render(request, 'admin/maintenanceman_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_maintenanceman(request):
    form = MaintenanceManModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_maintenanceman(request):
    mid = request.GET.get("mid")
    models.MaintenanceMan.objects.filter(mid=mid).delete()
    return redirect('/admin/maintenanceman/')                       


# =================维修委托单管理=================
def maintenance_order_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['orderId__contains'] = search_data
    queryset = models.MaintenanceOrder.objects.filter(**data_dict)
    form = MaintenanceOrderModelForm()

    return render(request, 'admin/maintenance_order_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_maintenance_order(request):
    form = MaintenanceOrderModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_maintenance_order(request):
    orderId = request.GET.get("orderId")
    models.MaintenanceOrder.objects.filter(orderId=orderId).delete()
    return redirect('/admin/maintenance_order/')                        


# =================维修派工单管理=================
def maintenance_workorder_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['workOrderId__contains'] = search_data
    queryset = models.MaintenanceWorkOrder.objects.filter(**data_dict)
    form = MaintenanceWorkOrderModelForm()

    return render(request, 'admin/maintenance_workorder_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_maintenance_workorder(request):
    form = MaintenanceWorkOrderModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_maintenance_workorder(request):
    workOrderId = request.GET.get("workOrderId")
    models.MaintenanceWorkOrder.objects.filter(workOrderId=workOrderId).delete()
    return redirect('/admin/maintenance_workorder/')   


# =================维修材料单管理=================
def usepart_list(request):
    data_dict = {}

    search_data = request.GET.get('query',"")
    if search_data:
        data_dict['partId__contains'] = search_data
    queryset = models.UseParts.objects.filter(**data_dict)
    form = UsePartsModelForm()

    return render(request, 'admin/usepart_list.html', 
                    {'queryset': queryset, 'search_data':search_data, 'form': form})

@csrf_exempt
def add_usepart(request):
    form = UsePartsModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

def del_usepart(request):
    nId = request.GET.get("nId")
    models.MaintenanceWorkOrder.objects.filter(nId=nId).delete()
    return redirect('/admin/usepart/')                      