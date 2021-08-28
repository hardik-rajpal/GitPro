from django.shortcuts import render

# Create your views here.
def signup(request):
    return render(request, 'signup.html')
def makeuser(request):
    dat = request.POST
    (username,password,fname,lname) = dat['username'], dat['password1'], dat['fname'], dat['lname']
    print(username, password, fname, lname)
    #store data here.
    print(request.POST)
    return render(request, "explore.html")
def loginpage(request):
    return render(request, 'loginpage.html')
def checkin(request):
    dat = request.POST
    print(request.POST)
    username, password = dat['username'], dat['password']
    #add logic to crosscheck credentials
    #if else clause
    return render(request, "explore.html")