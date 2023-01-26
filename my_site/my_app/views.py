from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseNotFound

# Create your views here.
def home_view(request):
    return HttpResponse("My_app Home View")

def show_template(request):
    return render(request,'my_app/example.html')

mobiles = {
    'Iphone_13':59900,
    'Iphone_14':69000,
    'Iphone_14_pro': 115000,
    'Iphone_14_pro_max': 189000,
}

def check_price(request,phone):
    try:
        result = mobiles[phone]
        return HttpResponse(result)
    except:
        return HttpResponseNotFound("Price has not been fixed yet!")
    
    