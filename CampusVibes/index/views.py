from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from login import settings
from django.contrib.auth.decorators import login_required
from index.forms import *
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django import forms
from django.utils.translation import ugettext_lazy as _
from index.models import *
from django.core.exceptions import ValidationError
from django.db.models.manager import Manager

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

       # username = clean_username(username)
       # clean(password1, password2)

        if form.is_valid():
            user = User.objects.create_user(username = username, email = email, first_name = first_name,
                                            last_name = last_name, password = password1)
            Login(request)
            #form.save()
            return HttpResponseRedirect('/home/')

    args = {}
    args.update(csrf(request))

    args['form'] = UserCreationForm()
    return render_to_response('index/register.html', args)

#def clean_username(username):
#    try:
#        user = User.objects.get(username__iexact = username)
#    except User.DoesNotExist:
#        return username
#    raise forms.ValidationError("The username already exists. Please try another one.")

#def clean(password1, password2):
#    if password1 and password2:
#        if password1 != password2:
#            raise forms.ValidationError("The two password fields did not match.")
#    return

def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            #raise forms.ValidationError(_("Incorrect username or password "))
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "index/login.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

@login_required
def Home(request):
    user = request.user
    logged_users = LoggedUser.objects.all().order_by('user')
    circle_users = MyCircle.objects.filter(userC = user)
    online_users = ['No online users']
    flag = 0
    for all_logged in logged_users:
        for all_circle in circle_users:
            if str(all_logged) == str(all_circle.username):
                flag = 1
                online_users.append(all_logged)
    if flag == 1:
        del online_users[0]
    return render(request, "index/home.html", {'output2': online_users})

@login_required
def add(request):
    user = request.user
    if request.method == "POST":
        username = request.POST['username']
        #try:
        #    already_user = User.objects.get(username__iexact = username)
        #except User.DoesNotExist:
        #    raise ValidationError(_(username+" does not exist. Please try again."))
        fname = User.objects.get(username=username).first_name
        lname = User.objects.get(username=username).last_name
        full_name = fname + ' ' + lname
        new_friend = MyCircle(userC = user, username = username, Uname= full_name)
        new_friend.save()

        nstring1 = 'You added '+username
        n1 = Notify(user = user, text = nstring1)
        n1.save()
        nstring2 = str(user)+' added you'
        user2 = User.objects.get(username=username)
        n2 = Notify(user = user2, text = nstring2)
        n2.save()

    return render(request, "index/add.html", {})

@login_required
def circle(request):
    user = request.user
    show = MyCircle.objects.filter(userC=user)
    return render(request, "index/circle.html", {'output': show})

@login_required
def chat_circle(request):
    user = request.user
    logged_users = LoggedUser.objects.all().order_by('user')
    show = MyCircle.objects.filter(userC=user)
    online_list = ['No online users']
    circle_list = ['No circle users']
    for item in logged_users:
        online_list.append(str(item))
    for item in show:
        circle_list.append(str(item.username))
    del online_list[0]
    del circle_list[0]

    return render(request, "index/chat_circle.html", {'output2': online_list, 'output': circle_list})

@login_required
def remove(request, username):
    user = request.user
    MyCircle.objects.filter(userC = user, username = username).delete()
    show = MyCircle.objects.filter(userC=user)

    nstring1 = 'You removed ' + username
    n1 = Notify(user=user, text=nstring1)
    n1.save()
    nstring2 = str(user) + ' removed you'
    user2 = User.objects.get(username=username)
    n2 = Notify(user=user2, text=nstring2)
    n2.save()

    return render(request, "index/circle.html", {'output': show})

@login_required
def notifications(request):
    user = request.user
    n = Notify.objects.filter(user = user)
    return render(request, "index/notifications.html", {'all': n})

@login_required
def clear_notifications(request):
    user = request.user
    Notify.objects.filter(user = user).delete()
    return render(request, "index/notifications.html", {})

@login_required
def chat(request, to_user='ChatRoom'):
    c = Chat.objects.filter(user = request.user, to_user__username = to_user)
    return render(request, "index/chat.html", {'home': 'active', 'chat': c, 'to_user': to_user})

@login_required
def clear_chat(request, to_user):
    Chat.objects.all().delete()
    return render(request, "index/chat.html", {'to_user': to_user})

@login_required
def Post(request, to_user=None):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg, to_user = to_user)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    c = Chat.objects.all()
    return render(request, 'index/messages.html', {'chat': c})
