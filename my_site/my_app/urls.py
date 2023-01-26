from django.urls import path
from . import views 

# It set's app namespace

app_name = "my_app"
urlpatterns = [
    path('',views.home_view,name="home-view"),
    path('template/',views.show_template,name="template"),
    #path('<str:phone>/',views.check_price, name="check_price"),
    
]