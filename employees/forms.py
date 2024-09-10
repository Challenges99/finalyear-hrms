from django.forms import ModelForm # modelform are used for html form 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.models import Profile, Attendance, Leave, Task
from django import forms



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields =['first_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self,*args,**kwargs):
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'TBox'})



class ProfileForm(ModelForm):
    class Meta:
        model= Profile
        fields= ['fname','lname','email', 'phone_no','account_no', 'account_name', 'address', 'state' ]


    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'profileTBox'})



class EmployeeDetailsForm(ModelForm):
    class Meta:
        model= Profile
        
        exclude = ['user', 'created','id','profile_image' ]
        labels = {
            'fname': 'First Name',
            'lname': 'Last Name'
        }

    def __init__(self,*args,**kwargs):
        super(EmployeeDetailsForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'answerTb'})



class EmployeeRegistrationForm(ModelForm):
    class Meta:
        model= Profile
        
        fields= '__all__'

    def __init__(self,*args,**kwargs):
        super(EmployeeRegistrationForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class': 'answerTb'})


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in_time', 'check_out_time', 'comment']
        widgets = {
            
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

 

class LeaveApplicationForm(forms.ModelForm):
    class Meta: 
        model= Leave
        fields= '__all__'

        exclude = ['employee','status'  ]

    def __init__(self,*args,**kwargs):
        super(LeaveApplicationForm,self).__init__(*args,**kwargs)

        field_styles= {
            
            'title': {'class': 'taskTitle'},
            'start_date': {'class': 'start-date-class', 'placeholder':'YYYY-MM-DD'},
            'end_date': {'class': 'end-date-class', 'placeholder':'YYYY-MM-DD'},
            'reason': {'class': 'taskDescription'},
            'comment': {'class': 'taskDescription'},
            'status': {'class': 'status-class'},
            'applied_on': {'class': ''},
        }

        for name,field in self.fields.items():
            if name in field_styles:
                field.widget.attrs.update(field_styles[name])
            else:
                field.widget.attrs.update({'class': 'taskTitle'})


class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model= Task
        fields= '__all__'

        exclude = ['status', 'assigner']

    def __init__(self,*args,**kwargs):
        super(TaskAssignmentForm,self).__init__(*args,**kwargs)

        field_styles= {
            
            'title': {'class': 'taskTitle'},
            'priority': {'class': 'taskPriority'},
            'assignee': {'class': 'assignee-class'},
            'deadline': {'class': 'start-date-class', 'placeholder':'YYYY-MM-DD'},
            'description': {'class': 'taskDescription'},
            'feedback': {'class': 'taskDescription'},
        }
        for name,field in self.fields.items():
            if name in field_styles:
                field.widget.attrs.update(field_styles[name])
            else:
                field.widget.attrs.update({'class': 'taskTitle'})