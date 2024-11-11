from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from crm.forms import EmployeeForm,SignupForm,SignInForm
from crm.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from  crm.decorators import signin_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.
decs=[signin_required,never_cache]
@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):

    template_name="employee_add.html"

    form_class=EmployeeForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"Created Successfully")

            return redirect("employee-list")
        
        messages.error(request,"Failed to create")
        
        return render(request,self.template_name,{"form":form_instance})
    
@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):

    template_name= "employee_list.html"

    def get(self,request,*args,**kwargs):

        qs=Employee.objects.all()

        return render(request,self.template_name,{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDetailView(View):

    template_name="employee_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        # qs=Employee.objects.get(id=id)

        qs=get_object_or_404(Employee,id=id)

        return render(request,self.template_name,{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        Employee.objects.get(id=id).delete()

        messages.success(request,"Deleted Successfully")

        return redirect("employee-list")

@method_decorator(signin_required,name="dispatch")
class EmployeeUpdateView(View):

    template_name="employee_update.html"

    form_class=EmployeeForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        employee_object=Employee.objects.get(id=id)

        form_instance=self.form_class(instance=employee_object)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):
         id=kwargs.get("pk")

         employee_object=Employee.objects.get(id=id)
         
         form_data=request.POST

         form_instance=self.form_class(form_data,files=request.FILES,instance=employee_object)

         if form_instance.is_valid():
             
             form_instance.save()

             messages.success(request,"updated Successfully")

             return redirect("employee-list")
         return render(request,self.template_name,{"form":form_instance})

class SignupView(View):

    template_name="Register.html"

    form_class=SignupForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
             
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data,files=request.FILES)

        if form_instance.is_valid():

            # form_instance.save()

            data=form_instance.cleaned_data

            User.objects.create_user(**data)

            return redirect("Register")
        
        return render(request,self.template_name,{"form":form_instance})

class SignInVIew(View):

    template_name="signin.html"

    form_class=SignInForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})
 
    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")
            pwd=data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("employee-list")
            
        return render(request,self.template_name,{"form":form_instance})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)
        
        return  redirect("signin")       















          






    






