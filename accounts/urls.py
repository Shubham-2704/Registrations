
from django.urls import path
from . import views  


urlpatterns = [
    path ('', views.index, name = 'index'),
    path ('login/', views.loginpage, name = 'login'),
    path ('signup/', views.signuppage, name = 'signup'),
    path ('forgotpassword/', views.forgotpassword, name = 'forgotpassword'),
    path ('resetpassword/<str:user>/', views.resetpassword, name = 'resetpassword'),
    path('logout/', views.logoutpage, name = "logout"),
    path('profile/', views.profilepage, name = "profile"),


]
