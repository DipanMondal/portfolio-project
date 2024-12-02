from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account-manager/', views.account_manager, name='account_manager'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('delete_feedback/<str:id>/', views.delete_feedback, name="delete_feedback"),
]
