from django.shortcuts import render, redirect
from taskapp.models import Task
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.

# def index(request):
#       return render (request,'index.html')
                      
def is_admin(user):
    return user.is_staff

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if is_admin(user):
                return redirect('admindashboard')
            else:
                return redirect('userdashboard')
        else:
            messages.error(request, "Incorrect login information")

    return render(request, 'Login.html')

# user = User.objects.get(username='zainab779')

# # Check if user is in a specific group
# if user.groups.filter(name='Software').exists():
#     print("User is in the group.")
# else:
#     print("User is not in the group.")


# Create groups for each section
# software_group, created = Group.objects.get_or_create(name='Software Admins')
# networking_group, created = Group.objects.get_or_create(name='Networking Admins')
# it_group, created = Group.objects.get_or_create(name='IT Admins')

# def login_view(request):
#     if request.method == "POST":
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(request, username=username,password=password)
        
#        if user is not None:
#         login(request,user)
#         return redirect('userdashboard')
#         messages.success(request, "Your login successfully.")    
#        else:
#              messages.error(request, "Incorrect login information")
              
#     return render(request, 'Login.html')

# @login_required(login_url='login')
# # @user_passes_test(lambda u: u.is_superuser, login_url='login')
# def admindashboard(request):
#     #    viewtask_data = Task.objects.filter(status='pending')
#         if request.user.groups.filter(name='Networking Admins').exists():
#             #  unassigned_tasks = Task.objects.filter(Q(section='networking')& Q( assign_to=User.objects.get(username='networkingadmin11@')))
#              unassigned_tasks = Task.objects.filter(Q(section='networking')& Q( status='pending')) 
#         elif request.user.groups.filter(name='Software Admins').exists():
#               unassigned_tasks = Task.objects.filter(Q(section='software')&Q( assign_to=User.objects.get(username='softwareadmin19@'))) 
#         data={'unassigned_tasks': unassigned_tasks}
#         return render(request, 'admindashboard.html',data)

@login_required(login_url='login')
def admindashboard(request):
    unassigned_tasks = None  # Initialize unassigned_tasks with a default value
    
    if request.user.groups.filter(name='Networking Admins').exists():
        unassigned_tasks = Task.objects.filter(Q(section='networking') & Q(status='pending')) 
    elif request.user.groups.filter(name='Software Admins').exists():
        unassigned_tasks = Task.objects.filter(Q(section='software') & Q(assign_to=User.objects.get(username='softwareadmin19@'))) 
    
    data = {'unassigned_tasks': unassigned_tasks}
    return render(request, 'admindashboard.html', data)


@login_required(login_url='login')
def userdashboard(request):
        if request.user.groups.filter(name='Networking Admins').exists():
          return redirect('admindashboard')
        elif request.user.groups.filter(name='Software Admins').exists():
          return redirect('admindashboard')
        
        tasks = Task.objects.filter(assign_to=request.user)
        viewtaskassign_data = Task.objects.filter(assign_to=request.user)
        mytask_data = Task.objects.filter(created_by=request.user)
        data={'tasks':viewtaskassign_data, 'mytask': mytask_data}

        #  assigned_tasks = Task.objects.filter(assign_to=request.user)
    #    networking_group = Group.objects.get(name='Networking')
    #    networking_users = networking_group.user_set.all()
    #    group = Group.objects.get(name='Networking')
    #    data={'tasks':viewtaskassign_data,}
        return render(request, 'userdashboard.html',data)  



# Networking Admin Dashboard
# @user_passes_test(lambda u: u.groups.filter(name='Networking Admins').exists(), login_url='login')
# def networking_admin_dashboard(request):
#     unassigned_tasks = Task.objects.filter(Q(section='networking') & Q( assign_to=User.objects.get(username='networkingadmin11@'))) 
#     context = {'unassigned_tasks': unassigned_tasks}
#     return render(request, 'networking_admin_dashboard.html', context)

# # Software Admin Dashboard
# # @user_passes_test(lambda u: u.groups.filter(name='Software Admins').exists(), login_url='login')
# def software_admin_dashboard(request):
#     unassigned_tasks = Task.objects.filter(Q(section='software')&Q( assign_to=User.objects.get(username='softwareadmin19@'))) 
#     context = {'unassigned_tasks': unassigned_tasks}
#     return render(request, 'software_admin_dashboard.html', context)

# create task
@login_required(login_url='login')
def create_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        status = request.POST.get('status')
        section_name = request.POST.get('section')
        priority = request.POST.get('priority')
        desc = request.POST.get('desc')
        #assign_to = request.user

        task = Task(
            title=title,
            status=status,
            section=section_name,
            priority=priority,
            desc=desc,
            created_by=request.user
        )
        
        # print(f"User Groups: {request.user.groups.all()}")
        if task.section == 'software':
           task.assign_to = User.objects.get(username='softwareadmin19@')
        elif task.section == 'networking':
            task.assign_to = User.objects.get(username='networkingadmin11@')
        
        task.save()
        messages.success(request, "Your task was created successfully.")
        return redirect('userdashboard')
  # if task.section:
        #      section = 'software'
        #      task.assign_to = User.objects.get(username='softwareadmin19@')
        # # if request.user.groups.filter(name='Software Admins').exists():
        # #     task.section = 'software'
        # #     task.assign_to = User.objects.get(username='softwareadmin19@')
        # #     print(f"Received Section from Form: {section_name}")
        # elif task.section:
        #      section = 'networking'
        #      task.assign_to = User.objects.get(username='networkingadmin11@')
        
        # # request.user.groups.filter(name='Networking Admins').exists():
        # #     task.section = 'networking'
        # #     task.assign_to = User.objects.get(username='networkingadmin11@')
        # task.save()

        # print(f"Task Section: {task.section}")
        # print(f"Task Assign To: {task.assign_to}")
    return render(request, 'create_task.html')



# @login_required(login_url='login')
# def create_task(request):
#     if request.method == "POST":
#         title = request.POST.get('title')
#         status = request.POST.get('status')
#         section_name = request.POST.get('section')
#         priority = request.POST.get('priority')
#         desc = request.POST.get('desc')
#         assign_to = request.user
#         task = Task(title=title, status=status, section=section_name, priority=priority, desc=desc, assign_to=assign_to, created_by=assign_to)
#         task.save()

#         messages.success(request, "Your task created successfully.")
#         return redirect('userdashboard')
#     else:
#         return render(request, 'create_task.html')
    

def details(request,id):
    #    taskdetail = Task.objects.get(id=id)
        group_name = request.user.groups.all()
        print('user group ', group_name)
        exclude_user = User.objects.get(username=request.user.username)
        users = User.objects.filter(groups__in=group_name).exclude(username=exclude_user.username)
    #    users = User.objects.all()
        # print('group name:', group_name[0])
        taskdetail = Task.objects.get(id=id)
        group_name = request.user.groups.all()
        # users = User.objects.all()

        if request.method == "POST":
         newuser_id = request.POST.get('assign_to')
         print('assigned', request.POST.get('assign_to'))

         print(f"Selected User ID: {newuser_id}")

         task = Task.objects.get(id=id)
         task.assign_to = User.objects.get(id=newuser_id)
         task.status = 'in-progress'
         task.save()
    #    section = Task.objects.values('section').distinct()
        # section_choices = Task.objects.values('section').distinct()
        data = {'task': taskdetail, 'users': users,}
        # group_name = request.user.groups.all()
       
        return render(request, 'details.html',data)

def userdetails(request,id):
       taskdetail = Task.objects.get(id=id)
       data={'task':taskdetail}
       return render(request, 'userdetails.html',data)


def assigntask(request):
      print('assigned', request.POST.get('assign_to'))
      task = Task.objects.filter(assign_to=request.user)
      assigntask_data = None 
      if request.user.groups.filter(name='Networking Admins').exists():
           exclude_user = User.objects.get(username='networkingadmin11@')
           assigntask_data = Task.objects.filter(Q(section='networking') & Q( status='in-progress')).exclude(assign_to=exclude_user)
      elif request.user.groups.filter(name='Software Admins').exists():
           exclude_user = User.objects.get(username='softwareadmin19@')
           assigntask_data = Task.objects.filter(Q(section='software') & Q( status='in-progress')).exclude(assign_to=exclude_user)
    #   if task.section == 'software':
    #     assigntask_data = Task.objects.filter(Q(section='software') & Q( status='pending'))
    #   elif task.section == 'networking':
    #    assigntask_data = Task.objects.filter(Q(section='networking') & Q( status='pending'))
           
    # #   assigntask_data = Task.objects.filter(Q(status='pending'))& Q(User.objects.get(id=))
      data={'tasks':assigntask_data}
      return render(request, 'assigntask.html',data)

def pending(request):
        pendingtask_data = Task.objects.filter(status='pending')
        pendingtask_data = None
        data = None
        if request.user.groups.filter(name='Networking Admins').exists():
            #  unassigned_tasks = Task.objects.filter(Q(section='networking')& Q( assign_to=User.objects.get(username='networkingadmin11@')))
            pendingtask_data = Task.objects.filter(Q(section='networking')& Q( status='pending')) 
        elif request.user.groups.filter(name='Software Admins').exists():
            pendingtask_data = Task.objects.filter(Q(section='software')&Q( assign_to=User.objects.get(username='softwareadmin19@'))) 
            data={'tasks':pendingtask_data}
        return render(request, 'pending.html',data)

def userpending(request):
        userpendingtask_data = None
        data = None
        userpendingtask_data = Task.objects.filter(status='pending')
        if request.user.groups.filter(name='Networking Admins').exists():
         userpendingtask_data = Task.objects.filter(Q(section='networking') & Q(status='pending')) 
        elif request.user.groups.filter(name='Software Admins').exists():
         userpendingtask_data = Task.objects.filter(Q(section='software') & Q(assign_to=request.user) & Q(status='pending')) 
        viewpending_data = Task.objects.filter(assign_to=request.user)
        mypending_data = Task.objects.filter(created_by=request.user)
        data={'tasks':viewpending_data, 'mytask': mypending_data,'task': userpendingtask_data}
        # data = {'task': userpendingtask_data}
        return render(request, 'userpending.html',data)


def resolved(request):
       resolvedtask_data = Task.objects.filter(status='completed')
       data={'tasks':resolvedtask_data}
       return render(request, 'resolved.html',data)

def userresolved(request):
        # userresolvedtask_data = None
        # data = None
        # if request.user.groups.filter(name='Networking Admins').exists():
        #  userpendingtask_data = Task.objects.filter(Q(section='networking') & Q(status='completed')) 
        # elif request.user.groups.filter(name='Software Admins').exists():
        #  userresolvedtask_data = Task.objects.filter(Q(section='software') & Q(assign_to=request.user) & Q(status='completed')) 
        # viewresolved_data = Task.objects.filter(assign_to=request.user)
        # myresolved_data = Task.objects.filter(created_by=request.user)
        # data={'tasks':viewresolved_data, 'mytask': myresolved_data,'task': userresolvedtask_data}
        # # data = {'task': userpendingtask_data}
        # return render(request, 'userresolved.html',data)
       resolvedtask_data = Task.objects.filter(status='completed')
       data={'tasks':resolvedtask_data}
       return render(request, 'userresolved.html',data)

def Logout_page(request):
      logout(request)
      return redirect('login')

# networking_group = Group.objects.get(name='Networking')
# software_group = Group.objects.get(name='Software')
# networking_admin_group = Group.objects.get(name='Networking Admin')
# software_admin_group = Group.objects.get(name='Software admin')
