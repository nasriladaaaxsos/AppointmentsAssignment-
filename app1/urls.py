from django.urls import path
from . import views	# the . indicates that the views file can be found in the same directory as this file
                    
urlpatterns = [
    path('', views.Index),    
    path('LoginUser', views.LoginUser), 
    path('Save', views.SaveUser),
    path('Viewall', views.ViewAll), 
    path('logout',views.logout),
    path('SaveShow', views.SaveShow),
    path('AddShow', views.AddShow),
    path('Get/<int:id>', views.GetShow), 
    path('Remove/<int:id>', views.DeleteShow), 
    path('Update/<int:id>', views.UpdateShow),
    path('Update', views.UpdateShowData),  
    path('Like/<int:id>', views.LikeShow),  

]