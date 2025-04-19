from django.urls import path

from . import swt_create
from . import views

urlpatterns = [
    path("", views.main_home, name="job-order-home"),
    path("jor/", views.job_order_form, name="job-order-form"),
    path("save/",views.save_job_order,name="save_job_order"),
    path("get/",views.get_num,name='get_num'),
    path("view/<str:job_order_number>/",views.view_job_order,name="view_job_order"),
    path("page_under_dev",views.page_under_dev,name="page_under_dev"),
    path("return_get/",views.return_get,name="return_get"),

    

    path("save_first_page/",swt_create.save_first_page,name="save_first_page"),
    path("checklist_development/<str:job_order_number>/",views.checklist_development,name="checklist_development"),
    path("swt2/<str:job_order_number>/",views.swt2,name="swt2"),
    path("update_second_page/",swt_create.update_second_page,name="update_second_page"),
    path("swt3/<str:job_order_number>/",views.swt3,name="swt3"),
    path("update_third_page/",swt_create.update_third_page,name="update_third_page"),
    path("swt4/<str:job_order_number>/",views.swt4,name="swt4"),
    path("update_fourth_page/",swt_create.update_fourth_page,name="update_fourth_page"),
    path("sucess/<str:job_order_number>/",views.sucess,name='sucess'),

    



]
