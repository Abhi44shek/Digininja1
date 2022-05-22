from django.shortcuts import render,redirect
from django.contrib import messages
from pytrends.request import TrendReq
from home.models import Search
import os
from django.contrib.auth.decorators import login_required
from plotly import graph_objects as go
import pandas as pd
import plotly.express as px
import tweepy


def get_trending_tweet(query):
    ck="<consumer-token>"
    cs= "<consumer-token-secret>"
    at = '<access-token>'
    ats= '<access-token-secret>'
    auth = tweepy.OAuthHandler(ck,cs,at,ats)
    api = tweepy.API(auth)
    results = api.search_tweets(query)
    print(len(results))
    if len(results) > 0:
        tweet_results = []
        for tweet in results:
            tweet_results.append({
                'tweet':tweet.text,
                'date':tweet.created_at,
                'retweets':tweet.retweet_count,
                'likes':tweet.favorite_count,
            })
        return tweet_results
    else:
        return None

# Create your views here.
@login_required
def index(request):
    return render(request,'home/index.html')



@login_required
def search(request):
    if request.method == 'POST':

        query = request.POST.get('query')
        if not query:
            messages.error(request, 'enter valid query!')
            return redirect('/')
        
        elif query:
            filepath = f'media/queries/{query}.json'
            filekeywords = f'media/queries/{query}_keywords.json'
            print('---->',not os.path.exists(filepath) and not os.path.exists(filekeywords))
            if not os.path.exists(filepath) or not os.path.exists(filekeywords):
                s = Search(query=query,user=request.user)
                s.save()
                pytrends = TrendReq(hl='en-US', tz=360)
                pytrends.build_payload([query], cat=0, timeframe='today 5-y', geo='IN', gprop='news')
                keywords = pytrends.suggestions(keyword=query)
                print(keywords)
                df = pytrends.interest_over_time()
                dfk = pd.DataFrame(keywords)
                if df is not None:
                    if not os.path.exists('media/queries'):
                        os.makedirs('media/queries')
                    df.to_json(filepath)
                    messages.success(request, 'data found.')
                else:            
                    messages.success(request, 'no data found.')
                if dfk is not None:
                    if not os.path.exists('media/queries'):
                        os.makedirs('media/queries')
                    dfk.to_json(filekeywords)
                    messages.success(request, 'keywords found.')
            else:
                messages.success(request, 'data found.')
            df_trend = pd.read_json(filepath)
            df_keywords = pd.read_json(filekeywords)
            fig = px.area(df_trend, x=df_trend.index, y=df_trend.columns[0], title=f'{df_trend.columns[0]} Searches over time')
            fig.update_layout({
                'height': 500,
            })
            ctx = {
                's':query,
                'fig':fig.to_html(),
                'df_trends':df_trend.tail(5)[[query]].to_html(),
                'df_keywords':df_keywords[['title','type']].to_html(),
                'tweet_results':get_trending_tweet(query),
            }
            return render(request,'home/search.html',context=ctx)
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




