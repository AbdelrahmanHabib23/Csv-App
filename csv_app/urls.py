from django.urls import path
from . import views

urlpatterns = [
    path('import/', views.import_accounts, name='import_accounts'),
    path('', views.list_accounts,
         name='list_accounts'),  # This is the URL pattern for the home page  
    path('accounts/<int:account_id>/', views.account_info,
         name='account_info'),
    path('transfer/', views.transfer_funds,
         name='transfer_funds'),  # Updated the path to 'transfer/'
    path('success/', views.success_view,
         name='success_url'),  # Ensure you have a success URL  
]
