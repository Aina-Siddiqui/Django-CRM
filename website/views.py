from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records=Record.objects.all()

    if request.method=='POST':
        username=request.POST['Username']
        password=request.POST['Password']
        #autenticate
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'you have been logged in')
            return redirect('home')
        else:
            messages.error(request,f"There was an error Logging in Please try again")
            return redirect('home')
    else: 
        return render(request,f'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out')
    return redirect('home')
def register_user(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,f'{{self.username}} registered successfully!')
            return redirect('home')
    else:

        form= SignUpForm()
        return render(request,f'register.html',{'form':form})
    return render(request,f'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        customer_record=Record.objects.get(id=pk)
        return render(request,f'record.html',{'customer_record':customer_record})
    else:
        messages.error(request,'You must be login to view that page')
        return redirect('home')
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Record Deleted Succcesfully')
        return redirect('home')
    else:
        messages.error(request,'Please Login First')
        return redirect('home')
def add_record(request):
    form=AddRecordForm(request.POST or None)
    
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                add_record=form.save()
                messages.success(request,'Record Added Successfully')
                return redirect('home')

        return render(request,'add_record.html',{'form':form})
    else:
        messages.error(request,'You must be login')
        return redirect('home')
def update_record(request,pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form=AddRecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,'Record Update Successfully')
            return redirect('home')
        return render(request,'update_record.html',{'form':form})

    else:
        messages.error(request,'You must be login')
        return redirect('home')

