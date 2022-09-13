from django.urls import path
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    path('', views.index),  
    path('Home', views.home),  
    path('LoginUser', views.LoginUser),    
    path('Save', views.SaveUser),   
    path('AddAppointment', views.AddAppointment),   
    path('SaveAppointment', views.SaveAppointment), 
    path('logout', views.logout), 
    path('Remove/<int:id>', views.DeleteAppoinment), 
    path('Update/<int:id>', views.UpdateAppointment),
    path('Update', views.UpdateAppointmentData),   
    path('Like', views.Like), 
    path('UnLike', views.UnLike), 
]