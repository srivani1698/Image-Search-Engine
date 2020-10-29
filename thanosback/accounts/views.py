"""from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .token_generator import account_activation_token

"""
from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your views here.
from .models import *
from .forms import CreateUserForm


#elastic search
from .etesting import eSearch
from .etesting import search
from .etesting import Data



        

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user = form.save()
            # username = form.cleaned_data.get('username')
            
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')


    else:
        form=CreateUserForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='login')
def viewProfile(request):
    return render(request, 'viewProfile.html')

@login_required(login_url='login')
def advanced(request):
    return render(request, 'accounts/advanced.html')

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')

def elastictest(request):
    results=[]
    epatentID=""
    epid=""
    print('--> ',request.POST)
    if request.POST.get('pid') and request.POST.get('patentID'):
        epatentID=request.POST.get('patentID')
        epid=request.POST.get('pid')
    elif request.POST.get('patentID'):
        epatentID=name=request.POST.get('patentID')
    elif request.POST.get('pid'):
        epid=request.POST.get('pid')
    results=eSearch(patentID=epatentID,pid=epid)
    print(results)
    context={
    'results':results,
    }
    return render(request,'accounts/advanced.html',context)



def maintest(request):
    res=[]
    epid=""
    if request.method == "POST":
        print(request.POST)
        if request.POST.get('pid'):
            epid=request.POST.get('pid')
    res=search(q=epid)
    context={
    'res':res,
    }
    return render(request,'accounts/dashboard.html', context=context)

def form(request):
    if request.method == "POST":
        print(request.POST)
        upload = request.FILES['upload']
        fs = FileSystemStorage()
        name = request.POST['patentID'] + '-D0' + str(request.POST['pid'])[2:]+'.png'
        print(name)
        fs.save(name, upload)
        if Data(request.POST):
            return HttpResponse('successfully updated')
        else:
            return HttpResponse('Failed!') 
    return render(request, 'accounts/form.html')

    




