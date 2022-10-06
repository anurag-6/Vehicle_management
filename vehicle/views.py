from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import VehicleForm
from .models import Vehicle
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from vehicle_manag import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required






def remove_spaces(string):
    strg = string.replace(" ", "")
    # also convert vh_number to uppercase
    return strg.upper()



def home(request):
    if  request.user.is_authenticated:
        if request.user.is_superuser :
            return redirect("sadminH")
        elif request.user.is_staff:
            return redirect("adminH")
        return redirect("userH") 
               
    return render(request,'index.html')


@login_required(login_url='/login')
def add_vehicle(request):
    if request.user.is_superuser:
        if request.method == "GET":
            form_obj = VehicleForm()
            context = {}
            context['form'] = form_obj

            return render(request,"super_admin/add_vehicle.html",context)
        elif request.method == "POST":

            # removing the white spaces from vehicle number
            mutable_query_set = request.POST.copy()
            mutable_query_set['vh_number'] = remove_spaces(mutable_query_set['vh_number'])

            vh_num = mutable_query_set['vh_number']

            form_data = VehicleForm(mutable_query_set)

            if Vehicle.objects.filter(vh_number=vh_num):
                messages.error(request,"Vehicle Already Exists")
                return redirect("addV")
            if form_data.is_valid():
                form_data.save()
                messages.success(request,"Vehicle Added Successfully!!")
                return redirect("addV")
            messages.error(request,VehicleForm.errors) 
            return redirect("addV")   
    return HttpResponse ("You dont have permission to accces this page")        

def sgup(request):
    if request.method == "GET":
        return render(request,'signup.html')
    elif request.method == "POST":
        un = request.POST['uname']  
        fn = request.POST['fname']  
        pw1 = request.POST['pwd1']
        pw2 = request.POST['pwd2']
        em = request.POST['em']


        if User.objects.filter(username=un):
            messages.error(request,"Username alredy taken,try another one")
            return redirect('sgup')

        if User.objects.filter(email=em):
            messages.error(request,"email alredy exists !!")
            return redirect('sgup')


        if pw1 != pw2:
            messages.error(request,"Confirm password didn't match !")
            return redirect('sgup')

        if len(un)>10:
            messages.error(request,"Username must be less than 10")
            return redirect('sgup')

        if not un.isalnum():
            messages.error(request,"Username must be alpha numeric ( 'A to Z and 0 to 9') ")
            return redirect('sgup')

        new_user = User.objects.create_user(username=un,first_name=fn,password=pw1,email=em)
        new_user.save()

        messages.success(request,"Your account has been successfully created!")

        # welcome mail 

        subject = "Welcome to Vehicle Management"
        message = "Hello" + new_user.first_name + "\n" + "Thankyou for Registering, Your Username is "+new_user.username 
        from_addr = settings.EMAIL_HOST_USER
        to_list = [new_user.email,]
        send_mail(from_email=from_addr,subject=subject,message=message,recipient_list=to_list)
        

        
        return redirect('lgin')


def lgin(request):
    if request.user.is_authenticated:
        return home(request)
    if request.method == 'GET':  
       return render(request,'login.html')
    elif request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']

        user = authenticate(username=un,password=pw)

        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('sadminH')
            elif user.is_staff:
                return redirect("adminH") 
            else:
                return redirect("userH")
        else:
            messages.error(request,"Incorrect Cradentials")   
            return redirect("lgin") 

@login_required(login_url='/login')
def view_vehicle(request):
    data = Vehicle.objects.all()
    return render(request,"view_vehicle.html",{'data':data})  

def lgout(request):
    logout(request) 
    return redirect("home") 

@login_required(login_url='/login')
def s_admin_home(request):
    if request.user.is_superuser:
        return render(request,'super_admin/super_admin_home.html')
    else:
        return HttpResponse("You dont have acccess to this page") 

@login_required(login_url='/login')
def admin_home(request):
    if request.user.is_staff:
        return render(request,'admin/admin_home.html')
    else:
        return HttpResponse("You dont have acccess to this page")   


@login_required(login_url='/login')
def user_home(request):
    if request.user.is_superuser:
        return redirect("sadminH")
    elif request.user.is_staff:
        return redirect("adminH") 
    else:       
        return render(request,'user/user_home.html')


     
@login_required(login_url='/login')
def edit_vehicle(request,vid):
    if request.user.has_perm('vehicle.change_vehicle'):
        if request.method == "GET":
            record = Vehicle.objects.get(id = vid)
            form_ob = VehicleForm(instance=record)
            return render (request,"edit_vehicle.html",{'form':form_ob})
        elif request.method == "POST":
            # getting the old record 
            record = Vehicle.objects.get(id = vid)
            form_ob = VehicleForm(instance=record)


            v_no = remove_spaces(request.POST['vh_number'])
            # Checking if the user edited the vh number. then
            #  checking for the new number is exist in the table,if present
            #    returning error
            if record.vh_number != v_no and Vehicle.objects.filter(vh_number=v_no):
                messages.error(request,"Vehicle Number alredy exits!!")
                return render (request,"edit_vehicle.html",{'form':form_ob})
                
            
            v_type = request.POST['vh_type']
            v_model = request.POST['vh_model']
            v_disc = request.POST['vh_disc']
            Vehicle.objects.filter(id=vid).update(vh_number=v_no,vh_type=v_type,vh_model=v_model,vh_disc=v_disc)
            
            msg = "Vehicle "+ v_no +" Edited successfully"
            messages.success(request,message=msg)

            return redirect("viewV")
    return HttpResponse('Permission denied for the user')        


        




            
@login_required(login_url='/login')
def del_vehicle(request,vid):
    if request.user.has_perm('vehicle.delete_vehicle'):
        Vehicle.objects.filter(id = vid).delete()
        messages.success(request,"Vehicle deleted Successfully")
        return redirect("viewV")
    return HttpResponse('Permission denied for the user')        
        
    







    

        


    


     