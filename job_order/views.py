from django.shortcuts import render

# Create your views here.
def home(request):
    
    return render(request, 'job_order/home.html')

def job_request(request):
    
    return render(request, 'job_order/job_request.html')