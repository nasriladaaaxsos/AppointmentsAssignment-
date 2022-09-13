from asyncio import Task
from asyncio.windows_events import NULL
from sqlite3 import Date
from django.db import models
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
import bcrypt
import re
from datetime import timedelta, date

class UserManager(models.Manager):
    def basic_validator_login(self, postData):
        errors = {}
        all_user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"    
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"    
        if len(all_user) and not bcrypt.checkpw(postData['password'].encode(), all_user[0].password.encode()):
            errors["passwordwronge"] = "Wrong Password!"   
        if not len(all_user):
            errors['emailnewuser'] = "Email is not registered" 
        return errors

    def basic_validator_reg(self, postData):
        errors = {}
        new_user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field       
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"  
        if len(postData['confirmpassword']) < 8:
            errors["confirmpassword"] = "Confirm Password should be at least 8 characters" 
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Last name should be at least 3 characters" 
        if len(postData['firstname']) < 3:
            errors["firstname"] = "First Name should be at least 3 characters" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if postData['password'] != postData['confirmpassword']:
            errors['password_confirm'] = "Password Dosent Match!"
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"
        if len(postData['confirmpassword']) == 0 :   
            errors["confirmpasswordrequired"] = "Confrim password is required!"
        if len(postData['lastname']) == 0 :   
            errors["lastnamerequired"] = "Last name is required!"
        if len(postData['firstname']) == 0 :   
            errors["firstnamerequired"] = "First name is required!"   
        if len(new_user):
            errors['emailnewuser'] = "Email already exist" 
        return errors

class AppointmentsManager(models.Manager):
    def basic_validator_save_appointment(self, postData):
        errors = {}
        if len(postData['Taskname']) == 0:
            errors["Taskname"] = "Task is required!"    
        if len(postData['Taskdate']) == 0 :   
            errors["Taskdate"] = "Date is required!"  
        if len(postData["Taskdate"]) > 0 and datetime.strptime(postData["Taskdate"], '%Y-%m-%d') <= datetime.today() :
            errors["birthday"] = "Invalid Date" 
        return errors


class User(models.Model):   
    firstname = models.TextField(max_length=255)
    lastname = models.TextField(max_length=255)
    email = models.CharField(max_length=45)
    password = models.TextField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)    
    objects = UserManager() 

class TaskStatus(models.Model):
    StatusDesc = models.TextField(max_length=255)  

class Appointments(models.Model):
    Taskname = models.TextField(max_length=255)
    Taskdate = models.DateTimeField(blank=True, null=True)    
    Taskuser = models.ForeignKey(User, related_name="users", default=1,on_delete = models.DO_NOTHING)
    Taskstatus = models.ForeignKey(TaskStatus, related_name="statues",default=1, on_delete = models.DO_NOTHING)
    objects = AppointmentsManager() 

class Like(models.Model):
    LikedAppointment = models.ForeignKey(Appointments, related_name="appoinments", on_delete = models.DO_NOTHING)
    LikedBy = models.ForeignKey(User, related_name="users1", on_delete = models.DO_NOTHING)

def user_login(formvalue): #request.POST   
        user_exist = User.objects.filter(email=formvalue.POST['email'])
        #print(user_exist.password)
        #print(formvalue.POST['password'].encode() )
        if user_exist:
            logged_user = user_exist[0] 
            if bcrypt.checkpw(formvalue.POST['password'].encode(), user_exist[0].password.encode()):
                print("password match")
                loggedin(formvalue,logged_user )
                return redirect('/Home')
                #messages.success(formvalue, "User successfully Logged")
            else:
                print("failed password")   
                return False            
        else:
            #print(user_exist[0].password)
            print("testtttttt")
            return False      

def save_user(formvalue): #request.POST    
    user_password = formvalue.POST['password']
    hash1 = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    print(user_password)
    u = User.objects.create(email = formvalue.POST['email'] ,password = hash1 ,created_date=datetime.now(), firstname = formvalue.POST['firstname'], lastname = formvalue.POST['lastname'] )
    formvalue.session['email'] = u.email
    formvalue.session['loggedin'] = 1
    formvalue.session['firstname'] = u.firstname
    formvalue.session['lastname'] = u.lastname
    formvalue.session['user_id'] = u.id

#def addstatus(request):
    #TaskStatus.objects.create(StatusDesc = "Missed")
    #TaskStatus.objects.create(StatusDesc = "Done")
    #NewUser = User.objects.get(id=1)
    #NewStatus = TaskStatus.objects.get(id=1)
    #Appointments.objects.create(Taskname = "Hello World", Taskdate=datetime.now, Taskuser = NewUser, Taskstatus = NewStatus )


def get_allAppointment(request):
    TaskUser_ = User.objects.get(id=request.session['user_id'])
    return Appointments.objects.filter(Taskuser=TaskUser_)

def loggedin(value, logged_user):
    value.session['email'] = value.POST['email']
    value.session['loggedin'] = 1
    value.session['firstname'] = logged_user.firstname
    value.session['lastname'] = logged_user.lastname
    value.session['user_id'] = logged_user.id

def get_allStatues():
    return TaskStatus.objects.all()

def save_appointment(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        statusid = request.POST['Taskstatus']
        print(userid,"---------------------",statusid)
        print(request.POST['Taskdate'])
        AppointmentStatus = TaskStatus.objects.get(id= statusid)
        AppointmentUser = User.objects.get(id= request.session['user_id'])
        Appointments.objects.create(Taskname = request.POST['Taskname'], Taskdate=request.POST['Taskdate'], Taskuser = AppointmentUser, Taskstatus = AppointmentStatus )


def getPastAppointment():
    input = Date.today()+ timedelta(days=1)
    print(input)
    return Appointments.objects.filter(Taskdate__range =[ "1900-01-01", input]  )

def remove_appointment(id):
    Appointment_selected = Appointments.objects.get(id=id)
    Appointment_selected.delete()

def update_appointment(id):
    Appointment_ = Appointments.objects.get(id=id)
    return Appointment_

def update_appointment_data(request):
    Appointment_ = Appointments.objects.get(id=request.POST['id'])
    Appointment_.Taskname = request.POST['Taskname']
    Appointment_.Taskdate = request.POST['Taskdate']
    #print(request.POST['Taskdate'])
    Status_ = TaskStatus.objects.get(id=request.POST['Taskstatus'])
    Appointment_.Taskstatus =  Status_
    Appointment_.save()

def addlike(request):
    print(request.POST['appoinmentid'])
    print(request.POST['id'])
    #Like.objects.create(LikedAppointment = 1, LikedBy = 1)

def removelike(request):
    print(request.POST['appoinmentid'])
    print(request.POST['id'])