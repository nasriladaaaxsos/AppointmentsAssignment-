from django.shortcuts import render,redirect
from . import models  # import model is important 
from django.contrib import messages
from django.shortcuts import render, HttpResponse

# index default page - website will start with it. 
def index(request):
    #models.addstatus(request)
    return render(request, "index.html")  

def LoginUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')          
        else: 
            user1 = models.user_login(request)
            if user1 is not False:     
                print("Logged in sucessfully")            
                return redirect('/Home')  
            else:
                print("Not logged in successfully")   
                return redirect('/')        
    print("Not Post requet")
    return redirect('/')   

def SaveUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')          
        else: 
            models.save_user(request)
            return redirect('/Home')  


#Get
def home(request):
    print("Here")
    if 'loggedin' in request.session:
        context = {
    	    "AllAppointment": models.get_allAppointment(request),
            "AllPastAppointment" : models.getPastAppointment(),
        }  
        return render(request, "home.html", context) 
    else:
        print("Not logged in") 
        return redirect('/')    

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        del request.session['loggedin']
        del request.session['firstname'] 
        del request.session['lastname'] 
        del request.session['user_id'] 
        print("Delete Session, Logout")     
    return redirect('/') 

#Get
def AddAppointment(request):
    if 'loggedin' in request.session:
        context = {
    	    "AllStatues": models.get_allStatues(),
        }  
        return render(request, "addappointment.html",context)
    else:
        print("Not logged in") 
        return redirect('/')  

def SaveAppointment(request):
    if request.method == "POST":  
        errors = models.Appointments.objects.basic_validator_save_appointment(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/AddAppointment')          
        else: 
            models.save_appointment(request)
            return redirect('/Home')

def DeleteAppoinment(request, id):
    models.remove_appointment(id),  
    return redirect('/Home') 

#Get
def UpdateAppointment(request, id):
    if 'loggedin' in request.session:
        context = {
            "updateappoitment": models.update_appointment(id),
            "AllStatues": models.get_allStatues(),
        }  
        return render(request, "UpdateAppointment.html", context)  
    else:
        print("Not logged in") 
        return redirect('/') 

def UpdateAppointmentData(request):
    if request.method == "POST":
        errors = models.Appointments.objects.basic_validator_save_appointment(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            #print('/Update/'+request.POST['id'])
            return redirect('/Update/'+request.POST['id'])          
        else: 
            models.update_appointment_data(request)
            return redirect('/Home')

def Like(request):
    print("0000000003333333333333333330000000000000000000000000")
    if request.method == "POST":
        models.addlike(request)
        return redirect('/Home')

def UnLike(request):
    if request.method == "POST":
        models.removelike(request)
        return redirect('/Home')