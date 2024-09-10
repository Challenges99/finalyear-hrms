from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Profile, Attendance, Leave,Task
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from.forms import CustomUserCreationForm,ProfileForm,EmployeeDetailsForm, AttendanceForm,LeaveApplicationForm, TaskAssignmentForm
from django.contrib.auth.models import User
# Create your views here.
def loginUser(request):
    if request.user.is_authenticated:
        pk=request.user.profile.id
        return redirect('dashboard',pk)

    if request.method== 'POST':
        email= request.POST['email']
        password= request.POST['password']
        
        try:
            user= User.objects.get(email=email)
        except:
            messages.error(request,'Username does not exist')

        user = authenticate(request, email= email, password=password)

        if user is not None:
            login(request,user)
            
            pk=request.user.profile.id
            return redirect('dashboard',pk)
        else:
             messages.error(request,'Username or password is incorrect')
     
    return render(request, 'employees/login.html')

@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    messages.info(request,'User has been logged out')
    return redirect('homepage')

def is_employer(user):
    return user.profile.role.lower() == 'employer'

def signupUser(request):
    form = CustomUserCreationForm()
    if request.method=='POST':
        form= CustomUserCreationForm(request.POST)
        if form.is_valid():
                user= form.save(commit= False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'User account was created')

                login(request, user)
                pk=request.user.profile.id
                return redirect('dashboard',pk)
            
        else:
            messages.success(request, 'An error has occured')
        
    context={'form':form, }
    return render(request, 'employees/signup.html',context)

def dashboard(request,pk):
    navbar_type="type1"
    profile= Profile.objects.get(id=pk)
    employees= Profile.objects.all()

    user_profile = Profile.objects.get(user=request.user)
    is_employer = user_profile.role=='employer'

    context={'navbar_type': navbar_type, 'employees':employees, 'profile': profile, 'is_employer': is_employer}
    return render(request,'employees/dashboard.html', context)


@login_required(login_url= 'login')
def EmployeeDetails(request,pk):
    navbar_type="type1"
    profile= Profile.objects.get(id=pk)

    user_profile = Profile.objects.get(user=request.user)

    is_employer = user_profile.role=='employer'
    
    form= EmployeeDetailsForm(instance= profile)
    if request.method== 'POST':
        form= EmployeeDetailsForm(request.POST,request.FILES, instance= profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile has been created Sucessfully')
            return redirect('user-profile')
        else:
            messages.error(request, 'Please correct the error below.')

    context= {'profile':profile,'navbar_type': navbar_type,'is_employer': is_employer, 'form': form }

    return render (request, 'employees/employeedetails.html', context)
    


@login_required(login_url= 'login')
@user_passes_test(is_employer, login_url='homepage')
def EmployeeRegistration(request):

    navbar_type="type1"
    form= EmployeeDetailsForm()
    if request.method == 'POST':
        form= EmployeeDetailsForm(request.POST)
        if form.is_valid():

            user= User.objects.create(
                username=form.cleaned_data['email'],
                email= form.cleaned_data['email']

            )
            user.set_password('12345abcde')
            user.save()

            profile = Profile.objects.create(
                user=user,
                fname=form.cleaned_data['fname'],
                lname=form.cleaned_data['lname'],
              
            )
            profile.save()

            if profile.role == 'employer':
                user.is_staff = True
                user.is_superuser = True
                user.save()

            messages.success(request, 'User account was created')
            return redirect('employee-registration')
        
        else: 
            messages.success(request, 'An error has occured')

    context={'navbar_type':navbar_type, 'form': form}
    return render (request, 'employees/employeeregistration.html', context)

    

@login_required(login_url= 'login')
def userProfile(request ):
    navbar_type="type2"
    profile = request.user.profile
    pagename = 'Profile'
    form = ProfileForm(instance=profile)     

    if request.method == 'POST':
        form= ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully')
            return redirect('user-profile')
        
        
    context= {'profile':profile,'navbar_type': navbar_type, 'form': form, 'pagename':pagename}
    return render (request, 'employees/profiles.html', context)

#employee directory

@login_required(login_url= 'login')
def employeedirectory(request):

    profiles= Profile.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    is_employer = user_profile.role=='employer'


    navbar_type="type1"
    context= {'profiles': profiles,'navbar_type': navbar_type, 'profile':user_profile, 'is_employer': is_employer}
    return render (request, 'employees/employeelist.html', context)

@login_required(login_url= 'login')
def attendancelist(request):

    profiles= Profile.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    is_employer = user_profile.role=='employer'
    pagename = 'Attendance'
    attendances = Attendance.objects.all().select_related('employee')
   

    navbar_type="type2"
    context= {'profiles': profiles,'navbar_type': navbar_type, 'profile':user_profile, 'pagename':pagename, 'attendances': attendances}
    return render (request, 'employees/attendancelist.html', context)


    
@login_required(login_url= 'login')
def attendancedetail(request, pk):
    
    user_profile = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(id=pk)
    is_employer = user_profile.role == 'employer'
    pagename = f'{profile.fname} {profile.lname} Attendance'

    attendances = Attendance.objects.filter(employee=profile)

    navbar_type = "type2"
    context = {
        'attendances': attendances,
        'navbar_type': navbar_type,
        'profile': user_profile,
        'profile': profile,
        'pagename': pagename,
        'is_employer': is_employer,
    }
    return render(request, 'employees/attendancedetails.html', context)


@login_required(login_url= 'login')
def signAttendance(request):
    navbar_type = "type2"
    profile = request.user.profile
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form= AttendanceForm(request.POST)
        if form.is_valid():
           attendance = form.save(commit=False)
           attendance.employee = user_profile

           # Calculate total hours
        check_in = form.cleaned_data.get('check_in_time')
        check_out = form.cleaned_data.get('check_out_time')
            
        if check_in and check_out:
            today = datetime.today().date()
            check_in_datetime = datetime.combine(today, check_in)
            check_out_datetime = datetime.combine(today, check_out)

            if check_out_datetime < check_in_datetime:
                check_out_datetime += timedelta(days=1)
            total_seconds = (check_out_datetime - check_in_datetime).total_seconds()
            total_hours = total_seconds / 3600

            attendance.total_hours = total_hours
            
        attendance.save()
        return redirect('attendance-list') 
    
    else:
        form= AttendanceForm()

    attendance_records = Attendance.objects.filter(employee=user_profile).order_by('-date')

    context={'form':form, 'navbar_type': navbar_type, 'profile': profile,}
    return render(request, 'employees/attendancecheckin.html', context )


@login_required(login_url='login')
def leaveApplication(request):
    profile = request.user.profile
    navbar_type = "type2"
    pagename = 'Leave Request'

    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = profile
            leave.save()
            return redirect('user-profile')
        else:
            print(form.errors)
    else:
        form = LeaveApplicationForm()

    context = {'form': form, 'profile': profile, 'navbar_type': navbar_type, 'pagename': pagename}
    return render(request, 'employees/leaverequest.html', context)

@user_passes_test(is_employer, login_url='homepage')
@login_required(login_url='login')
def leaveStatus(request):
    navbar_type = "type2"
    pagename = 'Leave Management'
    profile = request.user.profile
    leaves = Leave.objects.order_by('-applied_on') 
   
    if request.method == 'POST':
        leave_id= request.POST.get('leave_id')
        action = request.POST.get('action')
        leave = Leave.objects.get(id= leave_id, employee=profile)

        if action == 'accept':
            leave.status = 'Approved'
        elif action == 'reject':
            leave.status = 'Rejected'


        leave.save()
        return redirect('leave-management')

    context={'leaves': leaves, 'profile':profile, 'navbar_type': navbar_type, 'pagename': pagename }
    return render(request, 'employees/leavemanagement.html', context)               

@user_passes_test(is_employer, login_url='homepage')
@login_required(login_url='login')
def fullleaveStatus(request, leave_id):
    navbar_type = "type2"
    pagename = 'Leave Management'
    profile = request.user.profile
    leave = Leave.objects.get(id= leave_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            leave.status = 'Approved'
            leave.save()
            return redirect('leave-management')
        elif action == 'reject':
            leave.status = 'Rejected'
            leave.save()
            return redirect('leave-management')
        
        else:
            form = LeaveApplicationForm(request.POST, request.FILES, instance= leave)
            if form.is_valid():  
                leave.save()
                return redirect('leave-management')
    else:
        form = LeaveApplicationForm(instance=leave)
        
    context={'leave': leave, 'profile':profile, 'navbar_type': navbar_type, 'pagename': pagename, 'form':form }
    return render(request, 'employees/viewLeaveRequest.html', context)               


@login_required(login_url='login')
def create_task(request):
    navbar_type = "type2"
    pagename = 'Task Management'
    profile = request.user.profile
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigner= request.user.profile
            task.save()
            return redirect('user-profile')
    else:
        form= TaskAssignmentForm()

    context={'navbar_type': navbar_type, 'pagename': pagename, 'profile': profile, 'form': form}
    return render(request, 'employees/taskassign.html', context)



@login_required(login_url='login')
def view_tasks(request):
    navbar_type = "type2"
    pagename = 'Task Management'
    profile = request.user.profile
    user_profile = Profile.objects.get(user=request.user)

    tasks = Task.objects.filter(assignee=user_profile).order_by('start_date')

    context={'navbar_type': navbar_type, 'pagename': pagename,'profile':profile,'tasks':tasks}
    return render(request, 'employees/assigned_task.html', context)

@login_required(login_url='login')
def task_list(request):
    navbar_type = "type2"
    pagename = 'Task Management'
    profile = request.user.profile
    user_profile = Profile.objects.get(user=request.user)
    
    tasks = Task.objects.filter(assignee=user_profile).order_by('start_date')

    context={'navbar_type': navbar_type, 'pagename': pagename,'profile':profile,'tasks':tasks}

    return render(request,'employees/task_list.html', context)

@login_required(login_url='login')
def task_details(request, task_id):
    navbar_type = "type2"
    pagename = 'Task Management'
    profile = request.user.profile
    task = Task.objects.get(task_id=task_id)
    form = TaskAssignmentForm(instance=task)

    if request.method =='POST':
        form=TaskAssignmentForm(request.POST, request.FILES, instance= task)
        if form.is_valid():
            
            form.save()
            return redirect('assigned-task')
    # Fetch the specific task by ID
    

    context = {
        'navbar_type': navbar_type,
        'pagename': pagename,
        'profile': profile,
        'task': task,
        'form':form,
    }

    return render(request, 'employees/task_details.html', context)


    