import time
from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth.forms import UserCreationForm
 

def register(request):  
    print("The register view is being triggered.")
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        print("New user is being created.")
        if form.is_valid():  
            form.save()
            print("New user should have been created.")
            messages.success(request, 'Account created successfully')
            time.sleep(2)
            return redirect('login')
        else:
            context = {  
              'form':form  
            }
            return render(request, 'register.html', context)  
    else: 
        print("The else block is triggering.")
        form = UserCreationForm()  
        context = {  
            'form':form  
        }  
        return render(request, 'register.html', context)  

