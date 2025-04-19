from django.db import models
import os


class JOB_ORDER_FIRST_PAGE(models.Model):
    
    job_order_number=models.CharField(max_length=255,unique=True ,primary_key=True)
    date=models.DateField(auto_now_add=True)
    project=models.CharField(max_length=255)
    sensor=models.CharField(max_length=255)
    enow=models.CharField(max_length=255)
    required_by_date=models.DateField()
    request_provided_by=models.CharField(max_length=255)
    request_authorized_by=models.CharField(max_length=255)
    requirement=models.CharField(max_length=255)
    selected_inputs=models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.job_order_number}"


class SWT2(models.Model):

    job_order_number = models.OneToOneField(JOB_ORDER_FIRST_PAGE,verbose_name="job_order_number",related_name="swt2_job_order_number",  on_delete=models.CASCADE, db_column="job_order_number",primary_key=True)
    package = models.CharField(max_length=255,blank=True,null=True)
    version = models.CharField(max_length=255,blank=True,null=True)
    subsystem=models.CharField(max_length=255,blank=True,null=True)
            
    availability1 = models.BooleanField(default=False)
    sw_req_doc_remarks = models.TextField(blank=True, null=True,)

    availability2 = models.BooleanField(default=False)
    sw_des_doc_remarks = models.TextField(blank=True, null=True)

    availability3_1= models.BooleanField(default=False)
    src_base_doc_remarks = models.TextField(blank=True, null=True)

    availability3_2 = models.BooleanField(default=False)
    src_curr_remarks = models.TextField(blank=True, null=True)

    availability4 = models.BooleanField(default=False)
    tc_and_rep_remarks = models.TextField(blank=True, null=True)

    availability5 = models.BooleanField(default=False)
    ssrb_or_ssdrc_remarks = models.TextField(blank=True, null=True)

    availability6 = models.BooleanField(default=False)
    additional_remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.job_order_number} - {self.job_order_number.project} - {self.job_order_number.sensor} - {self.version} - {self.package}"


class SWT2Files(models.Model):
    
    
    def file_upload_path(instance,filename):
        """GENERATES a uniques upload path based on the file category"""
        safe_name_jo = instance.swt2.job_order_number.job_order_number  
        return os.path.join("uploads", safe_name_jo, instance.category, filename)  


    CATEGORY_CHOICES=[
        ("1.sw_req_doc","1_Software_Requirement_Document"),
        ("2.sw_des_doc","2_Software_Design_Document"),
        ("3_1.src_base_file","3_1_Source_Code_(Baseline_version)_Files"),
        ("3_2.src_curr_file","3_2_Source_Code_(Current_version)_Files"),
        ("4.tc_and_rep_doc","4_Test_Cases_and_Report_Files"),
        ("5.ssrb_or_ssdrc_doc","5_SSDRC/SSRB_Committee_minutes_and_closeouts_Files"),
        ("6.additional_doc","6_Additional_Files"),
    ]
    
    swt2 = models.ForeignKey(SWT2, on_delete=models.CASCADE, related_name="files", to_field="job_order_number", db_column="job_order_number")
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES,blank=True,null=True)
    file = models.FileField(upload_to=file_upload_path, blank=True, null=True) 
    status = models.CharField(max_length=50, default="NO File Attached",blank=True,null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.swt2.job_order_number} - {self.category} - {self.file if self.file else 'No File Attached'}"

class SWT3(models.Model):
    
    job_order_number = models.OneToOneField(JOB_ORDER_FIRST_PAGE,verbose_name="job_order_number",  on_delete=models.CASCADE, related_name="swt3_job_order_number",db_column="job_order_number",primary_key=True)
    date=models.DateField(auto_now_add=True)
    nature_of_work=models.TextField(blank=True,null=True)
    availability_of_inputs=models.CharField(max_length=255,blank=True,null=True)
    job_alloted_to=models.CharField(max_length=255,blank=True,null=True)
    date_of_commencement=models.DateField(blank=True,null=True)
    completion_date=models.DateField(blank=True,null=True)
    job_allotted_by=models.CharField(max_length=255,blank=True,null=True)
    job_authorized_by=models.CharField(max_length=255,blank=True,null=True)
    received_by=models.CharField(max_length=255,blank=True,null=True)
    comments=models.TextField(blank=True,null=True)


    def __str__(self):
        return f"{self.job_order_number} - {self.job_order_number.project} - {self.job_order_number.sensor} - {self.date} - {self.availability_of_inputs}"

class SWT4(models.Model):
    job_order_number = models.OneToOneField(JOB_ORDER_FIRST_PAGE,verbose_name="job_order_number", related_name="swt4_job_order_number", on_delete=models.CASCADE, db_column="job_order_number",primary_key=True)
    t_and_e_engineer=models.CharField(max_length=255,blank=True,null=True)
    rating=models.CharField(max_length=255,blank=True,null=True)
    subsystem=models.CharField(max_length=255,blank=True,null=True)
    signature=models.CharField(max_length=255,blank=True,null=True)   
    Remarks=models.TextField(blank=True,null=True)
 
