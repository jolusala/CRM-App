from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm


# Create your views here.
def Home(request):
    records = Record.objects.all()


    # Check to see if logging in
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In!")
            return redirect("home")
        else:
            messages.success(request,"There Was An Error Logging In, Please Try Again ...")
            return redirect("home")
        
    else:
        return render(request,"home.html",{"records":records})




def login_user(request):
    pass

def register(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request,"You Have Been Logged Out...")
    return redirect("home")

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record":customer_record} )
    
    else:
        messages.success(request,"You Must Be Logged In To View The Page")
        return redirect("home")

def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Record Deleted Successfully... ")
        return redirect("home")
    
    else:
        messages.success(request,"You Must Be Logged In To Delete")
        return redirect("home")
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect("home")
            

        return render(request, "add_record.html", {"form":form} )

    else:
        messages.success(request, "You Must Be Logged In ...")
        return redirect("home")
    
def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated...")
                return redirect("home")
        
        return render(request, "update_record.html", {"form":form} )

    else:
        messages.success(request, "You Must Be Logged In ...")
        return redirect("home")



