
from django.shortcuts import render ,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required




@login_required(login_url="/login/")
def zomato(request):
    if request.method == "POST":
        data = request.POST
        order_name = data.get('order_name')
        order_description = data.get('order_description')
        order_image = request.FILES.get('order_image')

        Order.objects.create(
            order_name =order_name,
            order_description =order_description,
            order_image = order_image
          )
        return redirect('/zomato/')
    
    queryset = Order.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(order_name__icontains = request.GET.get('search'))

    context = {'orders':queryset}
    
          


    return render(request,'zomato.html',context)

def update_order(request , id):
    queryset = Order.objects.get(id = id)
    context = {'order':queryset}

    if request.method == "POST":
        data = request.POST

        order_name = data.get('order_name')
        order_description = data.get('order_description')
        order_image = request.FILES.get('order_image')

        queryset.order_name = order_name
        queryset.order_description = order_description

        if order_image:
            queryset.order_image = order_image

        queryset.save()
        return redirect('/zomato/')    


    return render(request,'update_order.html',context)

def delete_order(request , id):
    queryset = Order.objects.get(id = id)
    queryset.delete()
    return redirect('/zomato/')

def login_page(request):

 if request.method == "POST":
     username = request.POST.get('username')
     password = request.POST.get('password')

     if  not User.objects.filter(username = username).exists():
         messages.error(request,"Ivaild Usename")
         return redirect("/login/")
     user = authenticate(username = username , password = password)

     if  user is None:
         messages.error(request ,"Invalid password")
         return redirect("/login/")
     else:
        login(request,user)

        return redirect("/zomato/")
    
 return render(request ,'login.html')  


def logout_page(request):
    logout(request)
    return redirect('/login/')
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user =User.objects.filter(username = username)

        if user.exists():
            messages.info(request,'username already taken')
            return redirect("register")


        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            

            
        )

        user.set_password(password)
        user.save()
        messages.info(request,'Account created Successfully')

        return render(request, 'register.html')
    return render(request ,'register.html') 