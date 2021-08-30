from datetime import datetime
from django.http import request

from django.http.request import HttpRequest
from othryz.models import Profile, Repository
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.forms import UserCreationForm
# from .models import UserProfile
# Create your views here.
def profile(request, profile_username):
    user = get_user(request)
    profile_user_obj = User.objects.get(username=profile_username)
    profileobj=Profile.objects.get(user=profile_user_obj)
    # repos = Repository.objects.filter()
    return render(request, "profile.html", {'repos':profileobj.repos, 'profile_username': profileobj.user.username, 'first_name':profileobj.user.first_name , 'last_name':profileobj.user.last_name ,'num_followers':profileobj.num_followers, 'last_updated':profileobj.last_updated})
def checkin(request):
    return render(request, "title.html")
def explore(request):
    userlist = []
    userobjs = User.objects.all()
    for user in userobjs:
        userlist.append(user.username)
    return render(request, "explore.html", {'users':userlist})
def updateProfile(request, user=None):
    if(user==None):
        user=get_user(request)
    user = User.objects.get(username=user.username)
    t = datetime.now()
    apiurl = 'https://api.github.com/users/' + user.username
    res = requests.get(apiurl)
    if(res.status_code!=200):
        print("Request for user failed")
        # return render(request, "error.html")
    data = res.json()
    num_followers = int(data['followers'])
    res = requests.get(apiurl + '/repos')
    if(res.status_code!=200):
        print("Request for repos failed")
        return
    data = res.json()
    reposdict = {str(x['name']):str(x['stargazers_count']) for x in data}
    print(reposdict, num_followers)
    profileobj,created = Profile.objects.get_or_create(user = user)
    profileobj.last_updated=t
    profileobj.num_followers=num_followers
    profileobj.repos=reposdict
    profileobj.save()
    for repo in reposdict:
        repobj, created = Repository.objects.get_or_create(user=profileobj, name=repo)
        repobj.stars = int(reposdict[repo]) 
        repobj.save()
    return redirect('/profile/' +  profileobj.user.username)
def register(request):
    print("hi")
    if request.method == 'POST':
        d = request.POST
        print(d)
        username = d['username']
        password = d['password1']
        fname = d['fname']
        lname = d['lname']
        user, created = User.objects.get_or_create(username=username,first_name=fname, last_name=lname)
        user.set_password(password)
        user.save()
        updateProfile(request, user)
        print(username, password, fname, lname)
        return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
        print(form)
        args = {'form':form}
        return render(request, 'registration/reg_form.html', args)