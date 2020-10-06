from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
import tweepy 
from . import private
import requests
import json
import re
from datetime import datetime
import tldextract
from .models import Tweet
from .models import Tweet_author
from django.db.models import Count


# Create your views here.

consumer_key = private.consumer_key 
consumer_secret = private.consumer_secret_key 


def home(request):
	return render(request, 'tweets/home.html')	



def oauth(request):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret,'http://127.0.0.1:8000/callback')
	redirect_url = auth.get_authorization_url()
	resposne=HttpResponseRedirect(redirect_url)
	request.session['request_token'] = auth.request_token
	return resposne



def callback(request):
	verifier = request.GET.get('oauth_verifier')
	if(verifier is None):
		return HttpResponseRedirect(reverse('tweets:login'))
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	token = request.session.get('request_token')
	request.session.delete('request_token')
	auth.request_token = token

	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error! Failed to get access token.')

	request.session['access_key']=auth.access_token
	request.session['access_key_secret']=auth.access_token_secret

	return HttpResponseRedirect(reverse('tweets:dashboard'))



# @login_required
def dashboard(request):
	if not checkkey(request):
		return HttpResponseRedirect(reverse('tweets:home'))

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

	access_token=request.session['access_key']
	access_token_secret=request.session['access_key_secret']
	  
	auth.set_access_token(access_token, access_token_secret) 
	  
	api = tweepy.API(auth, wait_on_rate_limit=True) 


	username = api.me().screen_name
	request.session['user']=username
	request.session['name']=api.me().name
	
	  
	statuses = api.home_timeline() 
	
	id_arr = []
	domain_arr = []
	Tweet.objects.all().delete()
	for tweetz in tweepy.Cursor(api.home_timeline).items(100):
		url = tweetz.entities['urls']
		if len(url) != 0:
			if url[0]['display_url'][0:7] != 'twitter' and allowTweet(tweetz):
				info = tldextract.extract(url[0]['expanded_url'])
				users = Tweet_author.objects.filter(person = tweetz.user.screen_name)
				if len(users) == 0:
					Tweet_author(person=tweetz.user.screen_name).save()
				tweetdata = Tweet(tweet_person=Tweet_author.objects.get(person=tweetz.user.screen_name), tweet_id = tweetz.id, tweet_domain=info.domain)
				tweetdata.save()
				id_arr.append(tweetz.id_str)



	top_authors = get_author()
	top_domains = get_domain()

	URL = 'https://publish.twitter.com/oembed?url=https%3A%2F%2Ftwitter.com%2FInterior%2Fstatus%2F'

	# for status in statuses:
	# 	id_arr.append(status.id_str)

	link_arr = []
	url_arr = []


	for i in range(len(id_arr)):
		x = URL+id_arr[i]
		r = requests.get(url=x).json()
		link_arr.append(r['html'])
	# link_arr=[]
	# top_authors=[]
	# top_domains=[]
	return render(request, 'tweets/dashboard.html',{'arr': link_arr, 'top_auth':top_authors, 'top_dom':top_domains})




def checkkey(request):
	try:
		access_key=request.session.get('access_key', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True


def allowTweet(tweet):
	x = (datetime.now() - tweet.created_at).days
	if x<8:
		return True
	else:
		False 

def get_author():
	q = Tweet.objects.all().values('tweet_person__person').annotate(total=Count('tweet_person__person')).order_by('-total')
	cnt=0
	data=[]
	for x in q:
		if cnt<3:
			data.append(x)
		else:
			break
		cnt+=1
	return data



def get_domain():
	q = Tweet.objects.all().values('tweet_domain').annotate(total=Count('tweet_domain')).order_by('-total')
	cnt=0
	data=[]
	for x in q:
		if cnt<3:
			data.append(x)
		else:
			break
		cnt+=1
	return data

