from django.shortcuts import render,redirect
from . import models  # import model is important 
from django.contrib import messages

# Create your views here.
from django.shortcuts import render, HttpResponse

def Index(request): 
        print("indexx^^^^^^^")
        return render(request, "User.html")  

def LoginUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/app1/')          
        else: 
            user1 = models.user_login(request)
            if user1 is not False:     
                print("HerereAmeeen")            
                return redirect('/app1/Viewall')  
            else:
                print("meshhoonAmeeen")   
                return redirect('/app1/')        
    print("Herere")
    return redirect('/app1/')   

def SaveUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/app1/')          
        else: 
            models.save_user(request)
            return redirect('/app1/Viewall')    


def ViewAll(request):
    context = {
    	"AllShows": models.get_allshow(),
    }  
    print("444444444444444444444444444444444444444444444",models.get_allshow())
    return render(request, "AllShows.html", context)  

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        del request.session['loggedin']
        del request.session['firstname'] 
        del request.session['lastname'] 
        del request.session['user_id'] 
        print("Delete Session, Logout")     
    return redirect('/app1/')   

def AddShow(request): 
        print("addshow^^^^^^^",request.POST)
        return render(request, "addshow.html")  

def SaveShow(request):
    if request.method == "POST":  
        errors = models.TVShow.objects.basic_validator_reg_show(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/app1/AddShow')          
        else: 
            models.save_show(request)
            return redirect('/app1/Viewall')

def GetShow(request, id):
    context = {
        "show": models.get_show(id),
    }
    request.session['added_by'] = models.get_added_by(id)   
    return render(request, "GetShow.html", context)  

def DeleteShow(request, id):
    context = {
    	"delete_show": models.remove_show(id),
    }  
    return render(request, "DeleteShow.html", context)  

def UpdateShow(request, id):
    print("^^^^^^^^^^",request.POST)  
    context = {
    	"updateshow": models.update_show(id),
    }  
    return render(request, "UpdateShow.html", context)  

def UpdateShowData(request):
    print("$$$$$$$$$$$",request.POST) 
    if request.method == "POST":
        print("$$$$$$$$$$$",request.POST) 
        models.update_show_data(request)
        return redirect('/app1/Viewall')

def LikeShow(request, id):
    context = {
    	"like_show": models.like_show(id, request),
    }  
    return render(request, "likeshow.html", context)  