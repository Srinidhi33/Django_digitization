
from job_order.views import swt3
from .models import SWT2, JOB_ORDER_FIRST_PAGE,SWT2Files,SWT3,SWT4
from datetime import date, datetime
from django.shortcuts import redirect,render
from django.http import JsonResponse
from .services import CRUD_SERVICES
from django.contrib.auth.decorators import login_required



@login_required
def save_first_page(request):
    if request.method=="POST":
        
        valid_data={key:value for key,value in request.POST.items() if hasattr(JOB_ORDER_FIRST_PAGE,key)}
            
        
        job_order_number=f"JOB_ORDER_{JOB_ORDER_FIRST_PAGE.objects.count()+1}"

        
        valid_data["job_order_number"]=job_order_number
        valid_data["selected_inputs"]=",".join(request.POST.getlist("selected_inputs"))
        valid_data["required_by_date"]=datetime.strptime(request.POST.get("required_by_date"), "%Y-%m-%d")
        
        # print(valid_data)
        
        crud_services.create_a_record(JOB_ORDER_FIRST_PAGE,{**valid_data})

            #get that instance of FIRST PAGE JOB_ORDER
        instance_of_first=JOB_ORDER_FIRST_PAGE.objects.get(job_order_number=job_order_number)
        
        #create a record in third page but with empty values excpet instance of first page
        crud_services.create_a_record(model=SWT3,valid_data={"job_order_number":instance_of_first})
        
        
        #create a record in fourth page but with empty values excpet instance of first page
        crud_services.create_a_record(model=SWT4,valid_data={"job_order_number":instance_of_first})
        
        if valid_data['requirement']=="Software CWT":

            #create a record in second page but with empty values excpet instance of first page
            crud_services.create_a_record(model=SWT2,valid_data={"job_order_number":instance_of_first})


        


            return redirect("swt2",job_order_number=job_order_number)
        else:
            return redirect("checklist_development",job_order_number=job_order_number)

@login_required
def update_second_page(request):
    
    
    
    if request.method=="POST":
        job_order_number=request.POST.get("job_order_number")
        
        valid_data={key:value for key,value in request.POST.items() if hasattr(SWT2,key)}

          
        file_data={
            "1_Software_Requirement_Document":request.FILES.getlist("1_Software_Requirement_Document"),
            "2_Software_Design_Document":request.FILES.getlist("2_Software_Design_Document"),
            "3_1_Source_Code_Baseline_Version_Files":request.FILES.getlist("3_1_Source_Code_Baseline_Version_Files"),
            "3_2_Source_Code_Current_Version_Files":request.FILES.getlist("3_2_Source_Code_Current_Version_Files"),
            "4_Test_Cases_and_Report_Files":request.FILES.getlist("4_Test_Cases_and_Report_Files"),
            "5_SSDRC_SSRB_Committee_Minutes_and_Closeouts":request.FILES.getlist("5_SSDRC_SSRB_Committee_Minutes_and_Closeouts"),
            "6_Additional_Documents":request.FILES.getlist("6_Additional_Documents")
                }
        
        # print(file_data)
        
        crud_services.update_a_record(model=SWT2,job_order_number=job_order_number,valid_data=valid_data)
        
        crud_services.update_files_record(SWT2,SWT2Files,job_order_number,file_data)
        
        return redirect("swt3",job_order_number=job_order_number)
        

@login_required
def update_third_page(request):
    
    job_order_number=request.POST.get("job_order_number")
    
    
    if request.method=="POST":
        
        valid_data={key:value for key,value in request.POST.items() if hasattr(SWT3,key)}
        
        crud_services.update_a_record(SWT3,job_order_number,valid_data)
        

        
        return redirect("swt4",job_order_number=job_order_number)
        

@login_required        
def update_fourth_page(request):
    job_order_number=request.POST.get("job_order_number")
    
    if request.method=="POST":
         
        # print(request.POST.items()) 
         
        valid_data={key:value for key,value in request.POST.items() if hasattr(SWT4,key)}
        
        # print({"valid data from views:":valid_data})        
        
        crud_services.update_a_record(SWT4,job_order_number,valid_data)

        return redirect("sucess",job_order_number=job_order_number)
    




crud_services=CRUD_SERVICES()
