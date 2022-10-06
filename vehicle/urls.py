from django.urls import path

from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('admin_home',views.admin_home,name='adminH'),
    path('s_admin',views.s_admin_home,name='sadminH'),
    path('user',views.user_home,name='userH'),
    path("add_vehicle/",views.add_vehicle,name="addV"),
    path("signup/",views.sgup,name="sgup"),
    path("login/",views.lgin,name='lgin'),
    path("view_vehicle/",views.view_vehicle,name='viewV'),
    path("logout/",views.lgout,name="lgout"),
    path("edit_vehicle/<int:vid>",views.edit_vehicle,name="editV"),
    path("del_vehicle/<int:vid>",views.del_vehicle,name="delV"),



    
]
