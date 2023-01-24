from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.db.models import Q


from .models import User
from .models import Thesis







def display_status(state):
    if(state=='0'):
        return "در انتظار تایید دانشجو"
    elif(state=='1'):
        return "در انتظار تایید استاد مشاور"
    elif(state=='2'):
        return "در انتظار تایید استاد راهنما"
    elif(state=='3'):
        return "در انتظار تایید مدیرگروه"
    elif(state=='4'):
        return "در انتظار کارشناس"
    elif(state=='5'):
        return "پایان فرآیند در سامانه"
    else:
        return "خطا"








def login(request):
    
    if request.method == 'POST':  
        # student = StudentForm(request.POST, request.FILES)  

        username = request.POST.get("username")
        password = request.POST.get("password")
        

        # mydata = User.objects.all().values()

        mydata = User.objects.filter(user_id=username ,password=password ).values()
        
        context = {
                'Error': "نام کاربری و یا رمز عبور صحیح نمی باشد",
             }

        if (mydata):

            user = User.objects.get(user_id=username)
            # num = request.session.get('u_id')
        
            request.session['u_id'] = username

            
            if (user.user_type=="0"):
                # print(request.context['request']._method)
                request.method = 'GET'
                return redirect(studentHome) #studentHome(request) 
            else:
                return redirect(userHome) #userHome(request) 
        else:
            template = loader.get_template('login.html')
            return HttpResponse(template.render(context, request))
            
    else:  
        template = loader.get_template('login.html')
        return render(request,'login.html')


def studentHome(request):
    u_id=request.session.get('u_id')
    if request.method == 'POST':  

    
        if request.POST.get('edit', ''):
            request.method = 'GET'
            return redirect(studentEdit)    #studentEdit(request) 
        elif request.POST.get('send', ''): 

            user = get_object_or_404(User, user_id=u_id)
            thesis = get_object_or_404(Thesis,student=user)
            thesis.state = "1"
            thesis.save()

            context = {
            'msg': "تایید شد",
             'thesis' : thesis,
            }
            template = loader.get_template('studentHome.html')
            return HttpResponse(template.render(context, request))

    else:  
        user = get_object_or_404(User, user_id=u_id)
        thesis = get_object_or_404(Thesis,student=user)
        
        context = {
            'thesis': thesis,
            'state': display_status(thesis.state),
                         'user': user,

            }
        template = loader.get_template('studentHome.html')
        return HttpResponse(template.render(context, request))




def studentEdit(request ):
    u_id=request.session.get('u_id')
    if request.method == 'POST':  
        user = get_object_or_404(User, user_id=u_id)
        thesis = get_object_or_404(Thesis,student=user)

        print("yes")
        t = request.POST.get('title')
        d = request.POST.get('description')
        f = request.POST.get('file')
        if(t):
            thesis.title = t
        if(d):
            thesis.description = d
        if(f):
            thesis.file = f
        if(f or d or t):
            thesis.save()
        request.method = 'GET'
        return redirect(studentHome) #studentHome(request)

    else:
        template = loader.get_template('studentEdit.html')
        return render(request,'studentEdit.html')


def userHome(request):
    u_id=request.session.get('u_id')
    user = get_object_or_404(User, user_id=u_id)
    thesis_adv = Thesis.objects.filter(advisor=user).values()
    thesis_sup = Thesis.objects.filter(supervisor=user).values()
    if(user.user_type =="3"):
        thesis_head = Thesis.objects.filter(state='3').values()
    else:
        thesis_head = []
    if(user.user_type =="2"):
        thesis_kar = Thesis.objects.filter(state='4',).values()
    else:
        thesis_kar = []    
    
    context = {
    'thesis_adv': thesis_adv,
        'thesis_sup': thesis_sup,
            'thesis_head': thesis_head,
             'thesis_kar': thesis_kar,
             'user': user,
    }
    request.method = 'GET'
    template = loader.get_template('userHome.html')
    return HttpResponse(template.render(context, request))


def advisor(request, id):
    u_id=request.session.get('u_id')
    if request.method == 'POST':  
        thesis = get_object_or_404(Thesis,id=id)

        if request.POST.get('back', ''):
            request.method = 'GET'
            return redirect(userHome)    #studentEdit(request) 
        elif request.POST.get('OK', ''): 
            print("ok")
            thesis.state = "2"
            thesis.save()
        elif request.POST.get('notOK', ''): 
            print("notOK")
            thesis.state = "0"
            thesis.save()

        request.method = 'GET'
        return redirect(userHome)
    else:
        user = get_object_or_404(User, user_id=u_id)
        thesis = get_object_or_404(Thesis,id=id)
        if(thesis.advisor == user):
            template = loader.get_template('advisor.html')
            context = {
                'thesis': thesis,
                'state': display_status(thesis.state),
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("اجازه دسترسی به این بخش را ندارید")

    
def supervisor(request, id):

    u_id=request.session.get('u_id')
    if request.method == 'POST':  
        thesis = get_object_or_404(Thesis,id=id)



        if request.POST.get('back', ''):
            request.method = 'GET'
            return redirect(userHome)    #studentEdit(request) 
        elif request.POST.get('OK', ''): 
            thesis.proposal_davar1 = get_object_or_404(User,user_id=request.POST.get("davar1"))
            thesis.proposal_davar2 = get_object_or_404(User,user_id=request.POST.get("davar2"))
            thesis.proposal_davar3 = get_object_or_404(User,user_id=request.POST.get("davar3"))
            thesis.proposal_davar4 = get_object_or_404(User,user_id=request.POST.get("davar4"))

            thesis.state = "3"
            thesis.save()
        elif request.POST.get('notOK', ''): 
            print("notOK")
            thesis.state = "0"
            thesis.save()

        request.method = 'GET'
        return redirect(userHome)
    else:
        users =  User.objects.filter(user_type='1').values() | User.objects.filter(user_type='3').values()
        user = get_object_or_404(User, user_id=u_id)
        thesis = get_object_or_404(Thesis,id=id)
        if(thesis.supervisor == user):
            template = loader.get_template('supervisor.html')
            context = {
                'thesis': thesis,
                'state': display_status(thesis.state),
                'users': users,
            }
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponse("اجازه دسترسی به این بخش را ندارید")

    
def karshenas(request, id):
    u_id=request.session.get('u_id')
    if request.method == 'POST':  
        thesis = get_object_or_404(Thesis,id=id)
        if request.POST.get('back', ''):
            request.method = 'GET'
            return redirect(userHome)  

    user = get_object_or_404(User, user_id=u_id)
    thesis =get_object_or_404(Thesis,id=id)
    if(user.user_type == "2"):
        template = loader.get_template('karshenas.html')
        context = {
            'thesis': thesis,
            'state': display_status(thesis.state),
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("اجازه دسترسی به این بخش را ندارید")



def head_of_department(request, id):
    u_id=request.session.get('u_id')
    if request.method == 'POST':  
        thesis = get_object_or_404(Thesis,id=id)

        if request.POST.get('back', ''):
            request.method = 'GET'
            return redirect(userHome)    #studentEdit(request) 
       
       
        elif request.POST.get('OK', ''): 
            thesis.davar1 = get_object_or_404(User,user_id=request.POST.get("davar1"))
            thesis.davar2 = get_object_or_404(User,user_id=request.POST.get("davar2"))

            thesis.state = "4"
            thesis.save()
            
        elif request.POST.get('notOK', ''): 
            print("notOK")
            thesis.state = "2"
            thesis.save()



        request.method = 'GET'
        return redirect(userHome)





    user = get_object_or_404(User, user_id=u_id)
    thesis = get_object_or_404(Thesis,id=id)
    if(user.user_type == "3"):
        template = loader.get_template('head_of_department.html')
        context = {
            'thesis': thesis,
            'state': display_status(thesis.state),
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("اجازه دسترسی به این بخش را ندارید")


    