"""dammsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from dammapp.views import account, customer, salesman, admin, maintenanceman, init

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 登录与注销
    path('', account.account_login),
    path('logout/', account.account_logout),
    path('register/', account.account_register),

    # 初始化数据
    path('init_account/', init.init_acccount),
    path('init_data/', init.init_data),

    # 管理员
    path('admin/', admin.admin_list),
    path('admin/add_admin/', admin.add_admin),
    path('admin/del_admin/', admin.del_admin),

    path('admin/worktype/', admin.worktype_list),
    path('admin/add_worktype/', admin.add_worktype),
    path('admin/del_worktype/', admin.del_worktype),

    path('admin/maintenance_item/', admin.maintenance_item_list),
    path('admin/add_maintenance_item/', admin.add_maintenance_item),
    path('admin/del_maintenance_item/', admin.del_maintenance_item),

    path('admin/parts/', admin.parts_list),
    path('admin/add_parts/', admin.add_parts),
    path('admin/del_parts/', admin.del_parts),

    path('admin/customer/', admin.customer_list),
    path('admin/add_customer/', admin.add_customer),
    path('admin/del_customer/', admin.del_customer),
    
    path('admin/customer_car/', admin.customer_car_list),
    path('admin/add_customer_car/', admin.add_customer_car),
    path('admin/del_customer_car/', admin.del_customer_car),

    path('admin/salesman/', admin.salesman_list),
    path('admin/add_salesman/', admin.add_salesman),
    path('admin/del_salesman/', admin.del_salesman),

    path('admin/maintenanceman/', admin.maintenanceman_list),
    path('admin/add_maintenanceman/', admin.add_maintenanceman),
    path('admin/del_maintenanceman/', admin.del_maintenanceman),

    path('admin/maintenance_order/', admin.maintenance_order_list),
    path('admin/add_maintenance_order/', admin.add_maintenance_order),
    path('admin/del_maintenance_order/', admin.del_maintenance_order),

    path('admin/maintenance_workorder/', admin.maintenance_workorder_list),
    path('admin/add_maintenance_workorder/', admin.add_maintenance_workorder),
    path('admin/del_maintenance_workorder/', admin.del_maintenance_workorder),

    path('admin/usepart/', admin.usepart_list),
    path('admin/add_usepart/', admin.add_usepart),
    path('admin/del_usepart/', admin.del_usepart),


    # 客户
    path('customer/', customer.customer_home),
    path('customer/edit_info/', customer.edit_info),
    path('customer/add_car/', customer.add_car),
    path('customer/add_order/', customer.add_order),
    path('customer/order_detail/', customer.order_detail),
    path('customer/order_list/', customer.order_list),

    # 业务员
    path('salesman/', salesman.salesman_home),
    path('salesman/order_detail/', salesman.order_detail),
    path('salesman/accept_order/', salesman.accept_order),
    path('salesman/finish_order/', salesman.finish_order),
    path('salesman/add_workorder/', salesman.add_workorder),
    path('salesman/edit_order/', salesman.edit_order),
    path('salesman/workorder_detail/', salesman.workorder_detail),
    path('salesman/edit_workorder/', salesman.edit_workorder),

    # 维修员
    path('maintenanceman/', maintenanceman.maintenanceman_home),
    path('maintenanceman/workorder_detail/', maintenanceman.workorder_detail),
    path('maintenanceman/start_workorder/', maintenanceman.start_workorder),
    path('maintenanceman/finish_workorder/', maintenanceman.finish_workorder),
    path('maintenanceman/add_usepart/', maintenanceman.add_usepart),
    path('maintenanceman/del_usepart/', maintenanceman.del_usepart),
]
