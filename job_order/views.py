import json
import os
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import datetime as dt
# from job_order import mir_services
from job_order.models import JOB_ORDER_FIRST_PAGE,  SWT2, SWT3, SWT4, SWT2Files
from .services import CRUD_SERVICES
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
 

@csrf_exempt
@login_required
def main_home(request):
    """Renders the Home page on top of Base.html"""
    job_order_numbers = []
    job_orders=JOB_ORDER_FIRST_PAGE.objects.all()
    for j in job_orders:
        job_order_numbers.append(str(j))    #TODO: Implenentation to be changed 
    """Renders the Home page on top of Base.html"""
    return render(request, 'job_order/home.html',context={"context":job_order_numbers})

@login_required
def job_order_form(request):
    """ Renders the Job Order Form with the current date from the server """
    current_date = dt.datetime.now()
    return render(request, "job_order/job_order_form.html", {"current_date": current_date})


# Define the JSON file path
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "job_orders.json")


@csrf_exempt
def save_job_order(request):
    """Handles form submission and save job order data with unique keys."""

    if request.method == "POST":
        try:
            raw_date = request.POST.get("required_by_date")
            formatted_date = datetime.strptime(raw_date, "%Y-%m-%d").strftime("%d-%m-%Y") if raw_date else None
            if os.path.exists(JSON_FILE_PATH):
                with open(JSON_FILE_PATH, "r") as json_file:
                    try:
                        job_orders_data = json.load(json_file)
                        if not isinstance(job_orders_data, dict):
                            job_orders_data = {}  # Reset if the structure is incorrect
                    except json.JSONDecodeError:
                        job_orders_data = {}  # Reset if file is empty or corrupted
            else:
                job_orders_data = {}

            # Generate a unique job order key (e.g., job_order_1, job_order_2, ...)
            job_order_number = len(job_orders_data) + 1
            # job_order_number = f"job_order_{job_order_numbers}"
            """ For Date conversion from 'str' to datetime object. """ 
            # print(request.POST.get("date")) 
            # a=datetime.strptime(request.POST.get("date"), "%d/%m/%Y")
            # print(a)
            # selected_inputs=",".join(re)
            new_job_order = {
                "job_order_number":job_order_number,
                "date": request.POST.get("date"),  # Date from server
                "project": request.POST.get("project"),
                "sensor": request.POST.get("sensor"),
                "exact_nature_of_work": request.POST.get("enow"),
                "required_by_date": formatted_date,
                "request_provided_by": request.POST.get("request_provided_by"),
                "request_authorized_by": request.POST.get("request_authorized_by"),
                "selected_requirement": request.POST.get("requirement"),
                "selected_inputs": ",".join(request.POST.getlist("selected_inputs"))
            }
            
            # print(request.POST.getlist("selected_inputs"))
            # print(type(request.POST.getlist("selected_inputs")))
            # # mylist=
            # total_str=",".join(request.POST.getlist("selected_inputs"))
            
            # for i in mylist:
            #     print(i)
            #     total_str=i.join(",")
            # print(total_str)
            
            # Load existing job orders if the file exists
            

            # Add the new job order with the unique key
            job_orders_data[job_order_number] = new_job_order

            # Save to JSON file
            with open(JSON_FILE_PATH, "w") as json_file:
                json.dump(job_orders_data, json_file, indent=4)
                if new_job_order['selected_requirement']=="software":
                    # return redirect("swt2",project_number=job_order_number,project=new_job_order['project'],sensor=new_job_order['sensor'],request_provided_by=new_job_order['request_provided_by'],request_authorized_by=new_job_order['request_authorized_by'])
                    # print("i am here")
                    # request.session['project']=new_job_order['project']
                    return redirect("swt2")
                else:
                    return redirect("sucess",job_order_number=job_order_number)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def get_num(request):
    """Render the HTML page that takes input for viewing JO"""
    if request.method=="POST":
            jo_num=request.POST.get("jo_num")
            job_order_number=f"JOB_ORDER_{jo_num}"
            
            return redirect("view_job_order",job_order_number=job_order_number)
            
    
    
    return render(request,"job_order/get.html")

@login_required
def view_job_order(request,job_order_number):
    
    try:
        # print(job_order_number)
        first_record=crud_services.read_a_record(model=JOB_ORDER_FIRST_PAGE,job_order_number=job_order_number)
        swt3_record=crud_services.read_a_record(model=SWT3,job_order_number=job_order_number)
        swt4_record=crud_services.read_a_record(model=SWT4,job_order_number=job_order_number)
        
        formatted_required_by_date = datetime.strptime(str(first_record.required_by_date), "%Y-%m-%d").strftime("%Y-%m-%d") if first_record.required_by_date else None
        formatted_date = datetime.strptime(str(first_record.date), "%Y-%m-%d").strftime("%d/%m/%Y") if first_record.date else None
        formatted_year=datetime.strptime(str(first_record.date),"%Y-%m-%d").strftime("%Y") if first_record.date else None
        swt3_record.completion_date=datetime.strptime(str(swt3_record.completion_date),"%Y-%m-%d").strftime("%Y-%m-%d") if swt3_record.completion_date else None
        swt3_record.date_of_commencement=datetime.strptime(str(swt3_record.date_of_commencement),"%Y-%m-%d").strftime("%Y-%m-%d") if swt3_record.date_of_commencement else None
        
        if first_record.requirement=="Software CWT":
            swt2_record=crud_services.read_a_record(model=SWT2,job_order_number=job_order_number)
            
            # expected_categories=["1.Software_Requirement_Document","2.Software_Design_Document","3_1.Source_Code_(Baseline_version)_Files","3_2.Source_Code_(Current_version)_Files","4.Test_Cases_and_Report_Files","5.SSDRC/SSRB_Committee_minutes_and_closeouts_Files","6.Additional_Files"]
            # files_by_category={category:[] for category in expected_categories}


            files_by_category={
                "1_Software_Requirement_Document":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="1_Software_Requirement_Document")
                    if file.file.name.strip()!=""
                    ],
                "2_Software_Design_Document":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="2_Software_Design_Document")
                    if file.file.name.strip()!=""
                    ],
                "3_1_Source_Code_Baseline_Version_Files":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="3_1_Source_Code_Baseline_Version_Files")
                    if file.file.name.strip()!=""
                    ],
                "3_2_Source_Code_Current_Version_Files":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="3_2_Source_Code_Current_Version_Files")
                    if file.file.name.strip()!=""
                    ],
                "4_Test_Cases_and_Report_Files":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="4_Test_Cases_and_Report_Files")
                    if file.file.name.strip()!=""
                    ],
                "5_SSDRC_SSRB_Committee_Minutes_and_Closeouts":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="5_SSDRC_SSRB_Committee_Minutes_and_Closeouts")
                    if file.file.name.strip()!=""
                    ],
                "6_Additional_Documents":[
                    {"url":file.file.url,"name":os.path.basename(file.file.name)}
                    for file in SWT2Files.objects.filter(swt2=swt2_record,category="6_Additional_Documents")
                    if file.file.name.strip()!=""
                    ]

            }
            # print(files_by_category["1_Software_Requirement_Document"])

            # for file in swt2_files_record:
            #     if file.category in files_by_category:
            #         files_by_category[file.category].append(file)




            l=[first_record,swt2_record,swt3_record,swt4_record]

            
            for i in l:
                i.year=formatted_year
                i.date=formatted_date
                i.required_by_date=formatted_required_by_date

            pages=[
                    {"template":"job_order/view_job_order.html","data":first_record},
                    {"template":"job_order/view_swt2.html","data":swt2_record,"files_by_category":dict(files_by_category)},
                    {"template":"job_order/view_swt3.html","data":swt3_record},
                    {"template":"job_order/view_swt4.html","data":swt4_record},
                ]

            paginator=Paginator(pages,1)
            page_number=request.GET.get("page",1)
            page_obj=paginator.get_page(page_number)

            return render(request,page_obj.object_list[0]["template"],{
                "record":page_obj.object_list[0]["data"],
                "files_by_category":page_obj.object_list[0].get("files_by_category",{}),
                "page_obj":page_obj,
                "read_only":True,
                "job_order_number":job_order_number
            })

        
        else:
            l=[first_record,swt3_record,swt4_record]

            for i in l:
                i.year=formatted_year
                i.date=formatted_date
                i.required_by_date=formatted_required_by_date



            pages=[
                    {"template":"job_order/view_job_order.html","data":first_record},
                    {"template":"job_order/view_checklist_development.html","data":first_record},
                    {"template":"job_order/view_swt3.html","data":swt3_record},
                    {"template":"job_order/view_swt4.html","data":swt4_record},
                ]

            paginator=Paginator(pages,1)
            page_number=request.GET.get("page",1)
            page_obj=paginator.get_page(page_number)

            return render(request,page_obj.object_list[0]["template"],{
                "record":page_obj.object_list[0]["data"],
                "files_by_category":page_obj.object_list[0].get("files_by_category",{}),
                "page_obj":page_obj,
                "read_only":True,
                "job_order_number":job_order_number
            })
            
    except Exception as e:
        print({"e":e})
        return redirect("return_get")


@login_required
def checklist_development(request,job_order_number):
   
    try:
        job_order=JOB_ORDER_FIRST_PAGE.objects.get(job_order_number=job_order_number) 
        
        context={
            "job_order_number":job_order.job_order_number,
            "requirement":job_order.requirement,
        }
        return render(request,"job_order/checklist_development.html",{"title":"Second page","context":context})
    except Exception as e:
        print({"e":e})


@login_required
def swt2(request,job_order_number):
    """Renders Second Page of Software Code Walkthrough"""
    job_order=JOB_ORDER_FIRST_PAGE.objects.get(job_order_number=job_order_number)  
    context={
        "job_order_number":job_order_number,
        "project":job_order.project,
        "provided":job_order.request_provided_by,
        "authorized":job_order.request_authorized_by
    }
    return render(request,"job_order/swt2.html",{"title":"Second page","context":context})


@login_required
def swt3(request,job_order_number):
    """Render Third Page of Software Code Walkthrough"""
    job_order=JOB_ORDER_FIRST_PAGE.objects.get(job_order_number=job_order_number)
    formatted_required_by_date=datetime.strptime(str(job_order.required_by_date),"%Y-%m-%d").strftime("%d/%m/%Y")
    if job_order.requirement=="software":
        requirement="Software CWT"
    # print(formatted_required_by_date)
    context={
        "requirement":job_order.requirement,
        "project":job_order.project,
        "sensor":job_order.sensor,
        "job_order_number":job_order_number,
        "required_by_date":formatted_required_by_date
    }
    
    return render(request,"job_order/swt3.html",{"title":"Third page","context":context})



@login_required
def swt4(request,job_order_number):
    """Render Fourth Page of Software Code Walkthrough"""
    job_order=JOB_ORDER_FIRST_PAGE.objects.get(job_order_number=job_order_number)
    context={
        "requirement":job_order.requirement,
        "project":job_order.project,
        "sensor":job_order.sensor,
        "enow":job_order.enow,
        "job_order_number":job_order_number
    }
    return render(request,"job_order/swt4.html",{"title":"Fourth page","context":context})


@login_required
def sucess(request,job_order_number):
    """Renders Success page after submission with the Job_order_number"""
    return render(request,"job_order/sucess.html", {"job_order_number":job_order_number })


def done(request):
    return render(request,"job_order/done.html")


@login_required
def return_get(request):
    return render(request,"job_order/return_get.html")

def dds(request):
    return render(request,"job_order/dds.html")

@login_required
def page_under_dev(request):
    """Renders temprovary Page under Development page"""
    return render(request,"job_order/page_under_dev.html") 


        
crud_services=CRUD_SERVICES()
# mir_services=mir_services.MIR_CRUD_SERVICES()
