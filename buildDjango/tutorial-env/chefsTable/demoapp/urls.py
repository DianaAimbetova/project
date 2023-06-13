from django.urls import path
from . import views

urlpatterns = [path('home/', views.home, name = 'home'),
               path('index/', views.index, name = 'index'),
                path("showform/", views.showform, name="showform"),
                path("getform/", views.getform, name='getform'),
                path("dishes/<str:dish>", views.menuitems),
                path('booking/', views.form_view),
                path('myview/', views.myview),
                path('newmyview/', views.newmyview),
                path('about/', views.about),
                path('menu/', views.menu),
                path('menucard/', views.menu_by_id),
                path('newview/', views.NewView.as_view()),
                path('create/', views.EmployeeCreate.as_view(), name = 'EmployeeCreate'),
]