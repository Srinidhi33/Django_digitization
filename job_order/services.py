from .models import JOB_ORDER_FIRST_PAGE, SWT2Files
from django.shortcuts import get_object_or_404

class CRUD_SERVICES:
    
    def __init__(self):
        self.parent=JOB_ORDER_FIRST_PAGE
        
    
    def create_a_record(self,model,valid_data:dict):
        
        return model.objects.create(**valid_data)
        
    def update_a_record(self,model,job_order_number,valid_data:dict):
        
        
        instance_of_first=get_object_or_404(self.parent,job_order_number=job_order_number)
        valid_data['job_order_number']=instance_of_first
        
        instance=get_object_or_404(model,job_order_number=job_order_number)
        
        
        
                  
        for key,value in valid_data.items():
            setattr(instance,key,value)
        
        
            
        instance.save()
        return instance
    
    def update_files_record(self,parent_model,model,job_order_number,file_data):
        
        #get parent instance ----> SWT2
        parent_instance=get_object_or_404(parent_model,job_order_number=job_order_number)
        
        # print({"file data":file_data})
        
        if file_data:
            
            for field,files in file_data.items():
                if files:
                    for file in files:
                    
                    
                        
                        SWT2Files.objects.create(
                            swt2=parent_instance, 
                            category=field,
                            file=file,
                            status="File Attached" if file else "NO File Attached")
                else:
                    SWT2Files.objects.create(swt2=parent_instance,category=field,file="",status="NO File Attached")
            # return instance
        else:
            print("didnt process")
            
    
    
    def read_a_record(self,model,job_order_number):
        
        return get_object_or_404(model,job_order_number=job_order_number)
    
    def delete_a_record(self,job_order_number):
        instance=get_object_or_404(self.parent,job_order_number=job_order_number)
        instance.delete()
        return f"Deleted successfully"
    
if __name__=="__main__":
    pass
