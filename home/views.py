from django.shortcuts import render,redirect
from django.contrib import messages

# Create your views here.
def index(request):
    if request.method == 'POST':
        email=request.POST.get('subscriber')
        if email and len(email)>10 and email.find('@')>0:
            sub = Subscriber(email=email)
            sub.save()
            messages.success(request, 'You have been successfully subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect('index')
    return render(request,'home/index.html')
def blog(request):
    return render(request,'home/blog.html')
def about(request):
    return render(request,'home/about.html')
def contact(request):
    return render(request,'home/contact.html')
def service(request):
    return render(request,'home/service.html')
def login(request):
    return render(request,'accounts/login.html')




