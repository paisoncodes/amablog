from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import AccountUpdateForm, RegistrationForm, AccountAuthenticationForm, OTPForm
from blog.models import Post
from .models import Account
from .utils import send_message, send_email

# Create your views here.

def registration_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    context={}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'authentication/signup.html', context)

def login_view(request):
    context={}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            remember_me = request.POST.get('remember_me', False)
            user = authenticate(username=username, password=password)

            if user:
                
                request.session['pk'] = user.pk
                request.session['remember_me'] = remember_me
                return redirect('verify')
                
    else:
        form = AccountAuthenticationForm
    
    context['login_form'] = form
    return render(request, 'authentication/signin.html', context)


def logout_request(request):
	logout(request)
	return redirect("home")

def account_view(request):

    user = request.user
    if not user.is_authenticated:
        return redirect('home')
    
    context = {}
    
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.initial={
                'email': request.POST['email'],
                'username': request.POST['username']
            }
            form.save()
            context['success_message'] = 'Update Successful!'
    else:
        form = AccountUpdateForm(
            initial={
                'email': user.email,
                'username': user.username
            }
        )
    
    context['account_form'] = form

    posts = Post.objects.filter(author=user)
    context['posts'] = posts

    return render(request, 'authentication/profile.html', context)



def must_authenticate_view(request):
    return render(request, 'authentication/must_authenticate.html', {})

def verification_view(request):
    context = {}
    form = OTPForm(request.POST or None)
    pk = request.session.get('pk')
    remember_me = request.session.get('remember_me')
    if pk:
        user = Account.objects.get(pk=pk)
        code = user.verificationcode
        code_user = f"{user.username}: {code}"

        if not request.POST:
            # send email
            send_email(user.username, code, user.email)

            # send sms
            send_message(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()

                login(request, user)
                
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('home')
            else:
                return redirect('signin')
        context['form'] = form

    return render(request, 'authentication/verification.html', context)