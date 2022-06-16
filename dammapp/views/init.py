from django.http import HttpResponse

from dammapp import models

# ============= data ============= 

mitems = [
        models.MaintenanceItem(itemName='检测汽缸压力'),
        models.MaintenanceItem(itemName='检修制动灯'),
        models.MaintenanceItem(itemName='更换机滤、机油'),
        models.MaintenanceItem(itemName='更换制动液'),
        models.MaintenanceItem(itemName='拆装或更换前轮制动片'),
        models.MaintenanceItem(itemName='拆装或更换后轮制动片'),
]

workType = [
        models.WorkType(typeName='电工', price=70),
        models.WorkType(typeName='机修', price=70),
        models.WorkType(typeName='钣金', price=70),
        models.WorkType(typeName='喷漆', price=70),
]

allparts = [
        models.Parts(partId='KP-01', partName='平衡轴垫片', partNumber=99, price=777),
        models.Parts(partId='KP-02', partName='前制动盘', partNumber=99, price=777),
        models.Parts(partId='KP-03', partName='后制动盘', partNumber=99, price=777),
        models.Parts(partId='KP-04', partName='右前制动盘防尘罩', partNumber=99, price=777),
        models.Parts(partId='KP-05', partName='左前制动盘防尘罩', partNumber=99, price=777),
        models.Parts(partId='KP-06', partName='右后制动盘防尘罩', partNumber=99, price=777),
        models.Parts(partId='KP-07', partName='右前门栏护板', partNumber=99, price=777),
        models.Parts(partId='KP-08', partName='左前门栏护板', partNumber=99, price=777),
]


def init_data(request):

        # for dc in mitems:
        #         models.MaintenanceItem.objects.create(**dc)
        # for dc in workType:
        #         models.WorkType.objects.create(**dc)
        # for dc in allparts:
        #         models.Parts.objects.create(**dc)

        models.MaintenanceItem.objects.bulk_create(mitems)
        models.WorkType.objects.bulk_create(workType)
        models.Parts.objects.bulk_create(allparts)

        return HttpResponse("Successful!")


def init_acccount(request):
    
    pwd_123456 = '33d7815def6759a80f20efa0731c3291'
    # init_admin
    admin = [models.Admin(name='admin', password=pwd_123456)]

    # init_customer

    cus = [models.Customer(customerName='Yelson', customerType=1, dicount=0.7, contactName='Yelson',
                         phone='19121807087', password=pwd_123456)]

    # init_salesman
    sls = [models.Salesman(sName='ys_s', phone='19121807087', password=pwd_123456)]

    # init_MaintenanceMan
    workType = models.WorkType.objects.first()
    mtm = [models.MaintenanceMan(mName='ys_m', phone='19121807087', password=pwd_123456, status=1, workType=workType)]

    # create
#     models.Admin.objects.bulk_create(admin)
#     models.Customer.objects.bulk_create(cus)
#     models.Salesman.objects.bulk_create(sls)
    models.MaintenanceMan.objects.bulk_create(mtm)
    
    return HttpResponse("Successful!")
