
from django.shortcuts import render
from django.shortcuts import redirect
from userauthentication.forms import UserRegisterForm,Profileform
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
# from django.contrib.auth.models import User
from userauthentication.models import Profile, User  

# from django.conf import settings
# User = settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid() :
            form.save()
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey{ username }, Your Account Created Successfuly")
            new_user = authenticate(username = form.cleaned_data["email"],  
                                    password = form.cleaned_data['password1'])
            
            login(request,new_user)    # logged in 
            return redirect("core:index")
        # else:
        #     print(form.errors)
    else:
        form = UserRegisterForm()
    
    context = {
    'form': form
    }
    return render(request,'userauthentication/register_page.html',context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"You are already logged in!")
        return redirect("core:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password= request.POST.get("password")

        try:
            user = User.objects.get(email =email)
            user = authenticate(request,email=email,password=password)    

            if user is not None:
                login(request,user)
                messages.success(request,"You are logged in")
                return redirect("core:index")
            else:
                messages.error(request,"Incorrect email or password!")
        except:
            messages.warning(request,f"User with {email} does not exist")

        
    context={
        
    }
    
    return render(request,'userauthentication/login.html',context)


def logout_view(request):
    logout(request)
    messages.success(request,f"You logged out")
    return redirect("userauthentication:login")


def profile_update(request):
    profile_photo = Profile.objects.get(user = request.user)
       
    if request.method== 'POST' :
        form = Profileform(request.POST,request.FILES,instance=profile_photo)
        if form.is_valid:
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request,"Profile updated succesfully")
            return redirect("core:dashboard")
        else:
            form = Profileform(instance=profile_photo)
    form = Profileform(instance=profile_photo)
    context = {
        "form":form,
        "profile_photo":profile_photo
    }
    return render(request,"userauthentication/profile-edit.html",context)

