from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotAllowed
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .myldap import *


def loginRequire(func):
    def wrapper(func,*args, **kwargs):
        if request.session.get('is_login', None):
            return func(*args, **kwargs)
        else:
            msg = '没登录就想改密码，你想多了！听话，先登录！'
            return render(request, 'login.html', locals())

def login(request):

    if request.method == 'GET':
        msg = ''
        logind = False
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        print(user, password)
        lrest = ldaplogin(user, password)
        if lrest == 0:
            if request.POST.get('remember') == '1':
                request.session.set_expiry(60)
            request.session['username']=user
            request.session['is_login']=True
            # # username = user
            # displayname = get_info(cn=user)[1]['displayName']
            # # # displayname = info[]['displayName']
            # msg = "欢迎： %s" %displayname
            return redirect('/setpwd.html')
        else:
            msg = "Invalid Password!"
            return render(request, 'login.html', locals())
    else:
        return HttpResponseNotAllowed('not support')


# @loginRequire
def setpassword(request):
    # if request.session.get('is_login', None):
    #     print(request.session)
    if request.method == 'GET':
            username = request.session.get('username')
            displayname = str(get_info(cn=username)[1]['displayName'][0], 'utf-8')
            return render(request, 'setpwd.html', locals())
    elif request.method == 'POST':
            result = ""
            username = request.POST.get('rusername')
            oldpassword = request.POST.get('oldpass')
            newpassword = request.POST.get('newpass')
            if username != request.session.get('username'):
                result = "您只能修改自己的密码！"
                username = request.session.get('username')
                return render(request, 'setpwd.html', locals())
            else:
                result = setpasswd(username, oldpassword, newpassword)
                return render(request, 'setpwd.html', locals())
    else:
            return HttpResponseNotAllowed("not support method!")
    # else:
    #     msg = '没登录就想改密码，你想多了！听话，先登录！'
    #     return render(request, 'login.html', locals())

def logout(request):
    request.session.clear()
    return render(request,'login.html',locals())