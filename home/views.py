from django.shortcuts import render,redirect
from django.contrib import messages
from pytrends.request import TrendReq
from home.models import Search
import os

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def search(request):
    if request.method == 'POST':

        query = request.POST.get('query')
        if not query:
            messages.error(request, 'enter valid query!')
            return redirect('/')
        
        elif query:
            filepath = f'media/queries/{query}.json'
            if not os.path.exists(filepath):
                s = Search(query=query,user=request.user)
                s.save()
                pytrends = TrendReq(hl='en-US', tz=360)
                kw_list = [query]
                pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='IN', gprop='news')
                df = pytrends.interest_over_time()
                if df is not None:
                    if not os.path.exists('media/queries'):
                        os.makedirs('media/queries')
                    df.to_json(filepath)
                    messages.success(request, 'data found.')
                else:            
                    messages.success(request, 'no data found.')
            return render(request,'home/search.html',context={'s':query})
    return redirect('/')


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




