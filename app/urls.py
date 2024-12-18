from django.contrib import admin  
from django.urls import path, include  

urlpatterns = [  
    path('admin/', admin.site.urls),  
    path('csv_app/', include('csv_app.urls')),  
]