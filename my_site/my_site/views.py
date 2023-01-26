from django.http.response import HttpResponse

def Entry_page(request):
    return HttpResponse("HOME VIEW")

def my_custom_page_not_found_view(request,exception=None):
    return render(request,'my_site/404.html',status = 404)
