from django.forms.utils import ErrorDict
from datetime import datetime
from .forms import GitProUserForm
from django.http.request import HttpRequest
from othryz.models import Profile, Repository
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
import requests
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
        return redirect('/dashboard/')
    return render(request, "dashboard.html")
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
def updateProfile(request, user=None):
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
        repo_dummy,created = Repository.objects.get_or_create(user=profileobj)
        repo_dummy.stars = 0
        repo_dummy.name='Your_Username_Is_not_accessible_on_Github'
        repo_dummy.save()
        return redirect('/profile/' +  profileobj.user.username + '/')
    apiurl = 'https://api.github.com/users/' + user.username
    try:
        res = requests.get(apiurl)
        res.raise_for_status()
    except requests.exceptions.RequestException as errh:
        return render(request, "error.html", {'message':f'Error in collecting User Data from Github \n {str(errh)}'})
    data = res.json()
    num_followers = int(data['followers'])
    res = requests.get(apiurl + '/repos')
    try:
        res = requests.get(apiurl + '/repos')
        res.raise_for_status()
    except requests.exceptions.RequestException as errh:
        return render(request, "error.html", {'message':f'Error in collecting Repository Data from Github \n {str(errh)}'})
    data = res.json()
    reposdict = {str(x['name']):str(x['stargazers_count']) for x in data}
    profileobj,created = Profile.objects.get_or_create(user = user)
    profileobj.last_updated=t
    profileobj.num_followers=num_followers
    profileobj.save()
    for repo in reposdict:
        repobj, created = Repository.objects.get_or_create(user=profileobj, name=repo)
        repobj.stars = int(reposdict[repo]) 
        repobj.save()
    return redirect('/profile/' +  profileobj.user.username + '/')

def register(request):
    form = GitProUserForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            password = cd.get('password1')
            fname = cd.get('first_name')
            lname = cd.get('last_name')
            user, created = User.objects.get_or_create(username=username,first_name=fname, last_name=lname)
            user.set_password(password)
            user.save()
            updateProfile(request, user)
            return redirect('/accounts/login/')
        else:
            errmsg = str(form.errors)
            errmsg = errmsg.replace("errorlist", "errorlist alert alert-danger")
            errmsg = errmsg.replace("password2", "password")
            return render(request, 'registration/reg_form.html', {'errmsg':errmsg, 'form':form})
    else:
        form = GitProUserForm()
        args = {'form':form}
        return render(request, 'registration/reg_form.html', args)