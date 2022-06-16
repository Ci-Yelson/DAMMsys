from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


#=================== 管理员表 ===================
class Admin(models.Model):
    ''''''
    aid = models.AutoField(verbose_name='业务员ID', primary_key=True, unique=True)
    name = models.CharField(verbose_name='姓名', max_length=64)
    password = models.CharField(verbose_name='密码', max_length=64)


#=================== 工种表 ===================
class WorkType(models.Model):
    ''''''
    typeId = models.AutoField(verbose_name='工种ID', primary_key=True, unique=True)
    typeName = models.CharField(verbose_name='工种名称', max_length=64)
    price = models.FloatField(verbose_name='工时单价')

    def __str__(self) -> str:
        return self.typeName


#=================== 维修项目表 ===================
class MaintenanceItem(models.Model):
    ''''''
    itemId = models.AutoField(verbose_name='维修项目ID', primary_key=True, unique=True)
    itemName = models.CharField(verbose_name='维修项目名称', max_length=64)

    def __str__(self) -> str:
        return self.itemName


#=================== 库存零件表 ===================
class Parts(models.Model):
    ''''''
    partId = models.CharField(verbose_name='零件编号', max_length=64, primary_key=True, unique=True)
    partName = models.CharField(verbose_name='零件名称', max_length=64)
    partNumber = models.IntegerField(verbose_name='零件数量')
    price = models.FloatField(verbose_name='零件单价')

    def __str__(self) -> str:
        return self.partName
    

#=================== 客户表 ===================
class Customer(models.Model):
    ''''''
    uid = models.AutoField(verbose_name='客户ID', primary_key=True, unique=True)
    customerName = models.CharField(verbose_name='客户名称', max_length=64, unique=True)
    type_choices = (
        (1, '个人'),
        (2, '单位'),
    )
    customerType = models.SmallIntegerField(verbose_name='客户性质', choices=type_choices, default=1)
    dicount = models.FloatField(verbose_name='折扣率')
    contactName = models.CharField(verbose_name='联系人', max_length=12)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self) -> str:
        return self.customerName


#=================== 客户车辆表 ===================
class CustomerCar(models.Model):
    ''''''
    vin = models.CharField(verbose_name='车架号', max_length=17, primary_key=True)
    lpn = models.CharField(verbose_name='车牌号', max_length=12)
    uid = models.ForeignKey(verbose_name='客户ID', to='Customer', to_field='uid', on_delete=models.CASCADE)
    color = models.CharField(verbose_name='颜色', max_length=12)
    carType = models.CharField(verbose_name='车型', max_length=12)
    category_choice = (
        (1, '微型车'),
        (2, '中型车'),
        (3, '大型车'),
    )
    category = models.SmallIntegerField(verbose_name='车辆类别', choices=category_choice, default=1)
    status_choice = (
        (1, '空闲'),
        (2, '正在维修'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)

    def __str__(self) -> str:
        return self.vin


#=================== 业务员表 ===================
class Salesman(models.Model):
    ''''''
    sid = models.AutoField(verbose_name='业务员ID', primary_key=True, unique=True)
    sName = models.CharField(verbose_name='业务员姓名', max_length=32)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self) -> str:
        return str(self.sid) + '-' + self.sName


#=================== 维修员表 ===================
class MaintenanceMan(models.Model):
    ''''''
    mid = models.AutoField(verbose_name='维修员ID', primary_key=True, unique=True)
    mName = models.CharField(verbose_name='维修员姓名', max_length=12)
    phone = models.CharField(verbose_name='联系电话', max_length=11)
    password = models.CharField(verbose_name='密码', max_length=64)
    workType = models.ForeignKey(verbose_name='工种', to='WorkType', to_field='typeId', on_delete=models.CASCADE)
    status_choice = (
        (1, '空闲'),
        (2, '工作中'),
        (3, '请假'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)

    def __str__(self) -> str:
        return str(self.mid) + '-' + self.mName


#=================== 维修委托单表 ===================
class MaintenanceOrder(models.Model):
    ''''''
    orderId = models.AutoField(verbose_name='维修委托单号', primary_key=True, unique=True)
    recordDate = models.DateField(verbose_name='登记日期', auto_now_add=True)
    vin = models.ForeignKey(verbose_name='车架号', to='CustomerCar', to_field='vin', on_delete=models.CASCADE)
    customerName = models.ForeignKey(verbose_name='客户名称', to='Customer', to_field='customerName', on_delete=models.CASCADE)
    customerPhone = models.CharField(verbose_name='客户联系电话', max_length=11)
    maintenance_choice = (
        (1, '普通'),
        (2, '加急'),
    )
    maintenanceType = models.SmallIntegerField(verbose_name='维修类型', choices=maintenance_choice, default=1)
    category_choice = (
        (1, '小修'),
        (2, '中修'),
        (3, '大修'),
    )
    category = models.SmallIntegerField(verbose_name='作业分类', choices=category_choice, default=1)
    payway_choice = (
        (1, '自付'),
        (2, '三包'),
        (3, '进保'),
    )
    payway = models.SmallIntegerField(verbose_name='结算方式', choices=payway_choice, default=1)
    mileage = models.IntegerField(verbose_name='进厂里程数')
    oil = models.FloatField(verbose_name='进厂油量')
    inDatetime = models.DateTimeField(verbose_name='进厂时间')
    sid = models.ForeignKey(verbose_name='业务员ID', to='Salesman', to_field='sid', 
                    null=True, blank=True, on_delete=models.SET_NULL)
    sName = models.CharField(verbose_name='业务员姓名', max_length=32, null=True, blank=True)
    phone = models.CharField(verbose_name='业务员联系电话', max_length=11, null=True, blank=True)
    
    finishDatetime = models.DateField(verbose_name='预计完工时间', null=True, blank=True)
    faultDiscribe = models.TextField(verbose_name='故障描述')
    cost = models.FloatField(verbose_name='维修总费用', null=True, blank=True)
    status_choic = (
        (1, '待受理'),
        (2, '正在维修'),
        (3, '已完成维修'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choic, default=1)


#=================== 维修派工单表 ===================
class MaintenanceWorkOrder(models.Model):
    ''''''
    workOrderId = models.AutoField(verbose_name='维修派工单ID', primary_key=True, unique=True)
    recordDate = models.DateField(verbose_name='发布日期', auto_now_add=True)
    startTime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    endTime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    orderId = models.ForeignKey(verbose_name='维修委托单ID', to='MaintenanceOrder', to_field='orderId', on_delete=models.CASCADE)
    itemId = models.ForeignKey(verbose_name='维修项目ID', to='MaintenanceItem', to_field='itemId', on_delete=models.CASCADE)
    sid = models.ForeignKey(verbose_name='业务员ID', to='Salesman', to_field='sid', on_delete=models.CASCADE)
    mid = models.ForeignKey(verbose_name='维修员ID', to='MaintenanceMan', to_field='mid', on_delete=models.CASCADE)
    hour = models.FloatField(verbose_name='工时')
    status_choice = (
        (1, '待开始'),
        (2, '进行中'),
        (3, '已完成'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice, default=1)
    artificialCost = models.FloatField(verbose_name='人工费', null=True, blank=True)
    totalPartsCost = models.FloatField(verbose_name='总材料费', null=True, blank=True)


#=================== 维修材料单表 ===================
class UseParts(models.Model):
    ''''''
    nId = models.AutoField(verbose_name='使用零件单ID', primary_key=True, unique=True)
    workOrderId = models.ForeignKey(verbose_name='维修派工单ID', to='MaintenanceWorkOrder', to_field='workOrderId', on_delete=models.CASCADE)
    partId = models.ForeignKey(verbose_name='零件编号', to='Parts', to_field='partId', on_delete=models.CASCADE)
    partNumber = models.IntegerField(verbose_name='零件数量')
    partCost = models.FloatField(verbose_name='零件费')


#=================== 使用Django的信号机制实现触发器 ===================
# noinspection PyUnusedLocal
# @receiver(post_save, sender=MaintenanceOrder)
# def pre_save_student(sender, instance, **kwargs):
#     '''post_save - 增加数据之后触发'''
#     '''申请委托后, 车辆的状态变为【正在维修】'''
#     car = instance.car
#     car.status = 2
#     car.save()