from datetime import datetime
from .forms import GitProUserForm
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
    repos = Repository.objects.filter(user=profileobj)
    repos_dict = {repo.name:repo.stars for repo in repos}
    return render(request, "profile.html", {'repos':repos_dict,'profile_username': profileobj.user.username, 'first_name':profileobj.user.first_name , 'last_name':profileobj.user.last_name ,'num_followers':profileobj.num_followers, 'last_updated':profileobj.last_updated})
def checkin(request:HttpRequest):
    if(request.path!='/dashboard/'):
        print(request.path)
        return redirect('/dashboard/')
    return render(request, "title.html")
def explore(request):
    userlist = []
    userobjs = User.objects.all()
    for user in userobjs:
        userlist.append(user.username)
    return render(request, "explore.html", {'users':userlist})
def gitHubAccExists(username):
    apiurl = 'https://api.github.com/users/' + username
    res = requests.get(apiurl)
    return res.status_code==200
def error(request):
    return render(request, "error.html")
def updateProfile(request, user=None, assign_dummy=False):
    t = datetime.now()
    if(user==None):
        user=get_user(request)
        user = User.objects.get(username=user.username)
    assign_dummy = not gitHubAccExists(user.username)
    if(assign_dummy):
        num_followers = 0
        profileobj,created = Profile.objects.get_or_create(user = user)
        profileobj.last_updated=t
        profileobj.num_followers=num_followers
        profileobj.save()
        repo_dummy = Repository.objects.create(name='Your_Username_Is_not_accessible_on_Github', stars=0, user=profileobj)
        repo_dummy.save()
        return redirect('/profile/' +  profileobj.user.username)

    apiurl = 'https://api.github.com/users/' + user.username
    res = requests.get(apiurl)
    if(res.status_code!=200):
        print("Request for user failed")
        return render(request, "error.html")
    data = res.json()
    num_followers = int(data['followers'])
    res = requests.get(apiurl + '/repos')
    if(res.status_code!=200):
        print("Request for repos failed")
        return render(request, "error.html")
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
    form = GitProUserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            password = cd.get('password1')
            print(password, cd.get('password2'))
            fname = cd.get('first_name')
            lname = cd.get('last_name')
            user, created = User.objects.get_or_create(username=username,first_name=fname, last_name=lname)
            user.set_password(password)
            user.save()
            if(gitHubAccExists(username)):
                updateProfile(request, user)
            else:
                # dummy_account = User.objects.get(username="JohnSmith007_abcxyz")
                updateProfile(request, user, assign_dummy=True)
            print(username, password, fname, lname)
            return redirect('/accounts/login/')
        else:
            print("validnot", form.errors)
            return redirect('/accounts/login/')
    else:
        form = GitProUserForm()
        print(form)
        args = {'form':form}
        # print("Hi")
        return render(request, 'registration/reg_form.html', args)