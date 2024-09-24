from django.shortcuts import render, redirect,get_object_or_404

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StateForm
from .models import StateCommittee, Volunteer, EndUser, State, Needs, User, Alert, Certificate,Complaint,EstimateCost,UserClaim,Task_voluenteer
from django.db.models import Q
from django.http import JsonResponse
# decorotors





def userOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 3:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view




def volunteerOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view




def stateCommitteeOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 1:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view



def adminOnly(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to the login page if user type doesn't match
    return _wrapped_view

def adminStateOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

def endUserOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 3 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

def adminStateVolunteerOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 or request.user.user_type == 2 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view

def adminStateUserOnly(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == 0 or request.user.user_type == 1 or request.user.user_type == 3 :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login') 
    return wrapped_view



# Create your views here.

""" ----VIEWS FOR ADMIN---- """

def landing(request):
    return render(request, 'base/user/landing.html')

@login_required(login_url='login')
@adminStateOnly
def home(request):

    
    if request.user.user_type == 0:
       endUsers = EndUser.objects.all()
    if request.user.user_type == 1:
        state_committee = StateCommittee.objects.get(host=request.user)
        state = state_committee.state

        endUsers = EndUser.objects.filter(state=state)
  
        
    context = {'endUsers' : endUsers,}

    return render(request, 'base/user/viewuser.html', context)


@login_required(login_url='login')
@adminOnly
def stateCommittee(request):

    stateCommittee = StateCommittee.objects.all()

    context = {'states' :stateCommittee,}
    

    return render(request, 'base/stateCommittee/viewStateCommittee.html', context)

@login_required(login_url='login')
@adminStateOnly
def volunteer(request):
    if request.user.user_type == 0 :

     volunteers = Volunteer.objects.all()
    
    if request.user.user_type == 1 :

        state_committee = StateCommittee.objects.get(host=request.user)
        state = state_committee.state 

        volunteers = Volunteer.objects.filter(state=state)

    context ={'volunteers':volunteers}


    return render(request, 'base/volunteer/viewVolunteer.html', context)


@login_required(login_url='login')
@adminStateOnly

def alerts(request):
    if request.user.user_type == 0:
         pendingAlerts = Alert.objects.filter(is_verified_by_admin=0, status=0)
         openAlerts = Alert.objects.filter(status=1)
         closedAlerts = Alert.objects.filter(status=2)
    if request.user.user_type == 1:
        stateCommittee = StateCommittee.objects.get(host=request.user)

        pendingAlerts = Alert.objects.filter(state_committee=stateCommittee, is_verified_by_state=0, status=0)
        data = Alert.objects.filter(host_id__isnull=True)
        print("Datas:", data)

        print("data",pendingAlerts)
        openAlerts = Alert.objects.filter(state_committee=stateCommittee, is_verified_by_state=1)
        closedAlerts = Alert.objects.filter(state_committee=stateCommittee, status=2)
        

    context = {
            'pendingAlerts':pendingAlerts,
            'data':data,
            'openAlerts' : openAlerts,
            'closedAlerts' : closedAlerts
    }

    return render(request, 'base/alerts/alerts.html', context)



def AssignVoluenteersbyadmin(request,pk):
    data = Volunteer.objects.all()
    
    alert_instance = Alert.objects.get(pk=pk)
    user_instance_id = request.user.id
   
    user_instance = User.objects.get(pk=user_instance_id)
    print(user_instance)
    
    if request.method == 'POST':
        datas = Task_voluenteer()
        vol=request.POST.get('volunteerid') 
        volunteer_instance = Volunteer.objects.get(userid=vol)
        alert_instance.is_verified_by_state = 1

        alert_instance.save()
        datas.volunteerid = volunteer_instance
        datas.alertid = alert_instance
        datas.userid = user_instance 
        datas.taskdescriprion = request.POST.get('taskdescriprion')
        datas.save()
      
        return redirect('/alerts')
    return render(request,'base/alerts/voluenteerassign.html',{'data':data,'alert_instance':alert_instance})

@login_required(login_url='login')
@adminStateOnly
def needs(request):

    if request.user.user_type == 0 :
        needs = Needs.objects.filter(is_verified_by_state=1, status=0)
        open_needs = Needs.objects.filter(status=1)
        closed_needs = Needs.objects.filter(status=2)
    if request.user.user_type == 1 :
        state_committee = StateCommittee.objects.get(host=request.user)
        needs = Needs.objects.filter(state_committee=state_committee, status=0, is_verified_by_state=0)
        open_needs = Needs.objects.filter(status=1, state_committee=state_committee)
        closed_needs = Needs.objects.filter(status=2, state_committee=state_committee)


    context = {
        'needs' : needs,
        'open_needs':open_needs,
        'closed_needs' : closed_needs
               
               }

    return render(request, 'base/needs/needs.html', context)



def addState(request):

    #setting all states

    states = State.objects.all()
    context = {'states': states}

    return render(request, 'base/stateCommittee/addState.html', context)


def addVolunteer(request):

    #setting all states

    states = State.objects.all()
    context = {'states': states}

    return render(request, 'base/volunteer/addVolunteer.html', context)



"""---------- STATE CRUD OPERATIONS -----------"""

# --- CREATE NEW STATE ---

def createState(request):

    if request.method == 'POST':

        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('number')
        stateid = request.POST.get('state')
        location = request.POST.get('location')
        state = State.objects.get(id=stateid)
        
        
        print('id', stateid)
        print('state', state)
        

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('add-state')

       
        else:
             user = User.objects.create_user(name=username,username=username, email=email, password=password)
             user.save()

             StateCommittee.objects.create(host=user,name=username,phone=phone, state=state, location=location)
             

             return redirect('statecommittee') 
        
      

# --- EDIT EXISTING STATE ---


@login_required(login_url='login')
@adminOnly
def editState(request, pk):
    stateCommittee = StateCommittee.objects.select_related('host').get(id=pk)
    user = stateCommittee.host
    
    states = State.objects.exclude(id=stateCommittee.state.id)
    

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/editstate/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/editstate/{pk}')

        # Update state and user data
        stateid = request.POST.get('state')
        state = State.objects.get(id=stateid)
        stateCommittee.name = request.POST.get('name')
        stateCommittee.phone = request.POST.get('number')
        stateCommittee.state = state
        stateCommittee.location = request.POST.get('location')

        user.email = email
        user.name = username
        user.set_password(request.POST.get('password'))

        stateCommittee.save()
        user.save()

        return redirect('statecommittee')

    context = {'user': user, 'stateCommittee': stateCommittee, 'states': states}

    return render(request, 'base/stateCommittee/editState.html', context)

# --- DELETE EXISTING STATE --- 
@login_required(login_url='login')
@adminOnly
def deleteState(request,pk):
    
    state = State.objects.get(id=pk)
    state.delete()
    return redirect('statecommittee')
    
        



#   ----------  STATE ENDS ------->

  

""" ---------- VOLUNTEER CRUD OPERATIONS ------ """

       

 # -----     DELETE EXISTING VOLUNTEER     -----

@login_required(login_url='login')
@adminStateOnly
def deleteVolunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    volunteer.delete()

    return redirect('volunteer')



#  ----- EDIT VOLUNTEER  -----


def editVolunteer(request, pk):
    volunteer = Volunteer.objects.select_related('host').get(id=pk)
    user = volunteer.host

    states = State.objects.exclude(id=volunteer.state.id)



    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/editvolunteer/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/editvolunteer/{pk}')

        # Update state and user data
        stateid = request.POST.get('state')
        volunteer.name = request.POST.get('name')
        volunteer.phone = request.POST.get('number')
        volunteer.state = State.objects.get(id=stateid)
        volunteer.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        volunteer.save()
        user.save()

        return redirect('volunteer')

    context = {'user': user, 'volunteer': volunteer, 'states':states}

    return render(request, 'base/volunteer/editVolunteer.html', context)
           

   
   
   
"""  ----  END USER CRUD OPERATIONS    ----- """

# ----    DELETE EXISTING USER    ---- 
@login_required(login_url='login')
@adminStateOnly
def deleteUser(request, pk):
    user = EndUser.objects.get(id=pk)
    user.delete()
    return redirect('/')


# edit Enduser  

def editEndUser(request, pk):
    enduser = EndUser.objects.select_related('host').get(id=pk)
    user = enduser.host
    states = State.objects.exclude(id=enduser.state.id)

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('name')

        # Check if the given email is already taken by another user
        existing_user = User.objects.filter(email=email).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Email Already Taken')
            return redirect(f'/edituser/{pk}')

        # Check if the given username is already taken by another user
        existing_user = User.objects.filter(username=username).exclude(pk=user.pk).first()
        if existing_user:
            messages.info(request, 'Username Already Taken')
            return redirect(f'/edituser/{pk}')
        

        stateid = request.POST.get('state')
        # Update state and user data
        enduser.name = request.POST.get('name')
        enduser.phone = request.POST.get('number')
        enduser.state = State.objects.get(id=stateid)
        enduser.location = request.POST.get('location')

        user.email = email
        user.username = username
        user.set_password(request.POST.get('password'))

        enduser.save()
        user.save()

        return redirect('/')

    context = {'user': user, 'enduser': enduser, 'states':states}

    return render(request, 'base/user/editEndUser.html', context)





""" ------     HOME PAGES     ------ """

#Login Page




def loginPage(request):
   
    if request.user.is_authenticated:
         print(request.user.user_type )
         if request.user.user_type == 3:
           return redirect('user-home')
         elif request.user.user_type == 2:
             return redirect('volunteer-home')
         else:
             return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        
        user_login = authenticate(request, email=email, password=password)

        if user_login is not None:
            login(request, user_login)
            if user_login.user_type == 3:
                return redirect('user-home')
            elif user_login.user_type == 2:
                return redirect('volunteer-home')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
 
    return render(request, 'Front/Login.html')

#Register Pages

# State Register Page

def stateRegister(request):

    states = State.objects.all()
    context = {'states': states}

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        stateid = request.POST.get('state')
        name = request.POST.get('name')    
        phone = request.POST.get('number')
        state = State.objects.get(id=stateid)
        location = request.POST.get('location')
        email = request.POST.get('email')
        password = request.POST.get('password')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        usertype =request.POST.get('usertype')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Taken')
            return redirect('state-register')
        elif User.objects.filter(username=name).exists():
            messages.info(request, 'Username Already Taken')
            return redirect('state-register')
        
        else:
            user = User.objects.create_user(username=name, name=name, user_type=usertype, email=email, password=password)
           
            state_committee = StateCommittee.objects.create(host=user, name=name, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
             
            user.save()
            state_committee.save()
            login(request, user)

            return redirect('home')
        



    return render(request, 'base/stateCommittee/stateRegister.html', context)

#VOLUNTEER REGISTER PAGE

def register(request):
    states = State.objects.all()
    context = {'states': states}

    if request.user.is_authenticated:
        return render('volunteer-home')

    if request.method == 'POST':
       
       stateid = request.POST.get('state')
       

       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = State.objects.get(id=stateid)
       location = request.POST.get('location')
       email = request.POST.get('email')
       password = request.POST.get('password')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       usertype = request.POST.get('usertype')
       

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('register')
       if User.objects.filter(username=username).exists():
           messages.info(request, 'username already Taken')
           return redirect('register')
      
       else:
           user = User.objects.create_user(name=username,username=username, email=email,user_type=usertype, password =password)
           user.save()
        #    user =user.id
        #    print(user)
           Volunteer.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude,userid=user)
           login(request, user)

           return redirect('volunteer-home')

    




    return render(request, 'Front/register.html', context)


#User Register Page


def userRegister(request):

     states = State.objects.all()
     context = {'states': states}

     if request.user.is_authenticated:
         return redirect('user-home')

     if request.method == 'POST':
       
       stateid = request.POST.get('state')
       

       username = request.POST.get('name')
       phone = request.POST.get('number')
       state = State.objects.get(id=stateid)
       location = request.POST.get('location')
       email = request.POST.get('email')
       password = request.POST.get('password')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       user_type = request.POST.get('usertype')

       print('latitude', latitude)
       print('longitude', longitude)

       if User.objects.filter(email=email).exists():
           messages.info(request, 'Email already taken')
           return redirect('user-register')
       elif User.objects.filter(username=username).exists():
           messages.info(request, 'username already taken')
           return redirect('user-register')
       else:
           user = User.objects.create_user(username=username,name=username,user_type=user_type, email=email, password=password)
           user.save()
           EndUser.objects.create(host=user, name=username, phone=phone, state=state, location=location, latitude=latitude, longitude=longitude)
           login(request, user)

           return redirect('user-home')


     return render(request, 'Front/User/userRegister.html',context)


# Logout user

@login_required(login_url='login')
def logoutUser(request):
    logout(request)

    return redirect('login')


# VOLUNTEER HOME PAGE

@login_required(login_url='login')
@volunteerOnly
def volunteerHome(request):
    
    volunteer = Volunteer.objects.get(host=request.user)
    
    pendingNeeds = Needs.objects.filter(host=volunteer,status=0)

    activeNeeds = Needs.objects.filter(host=volunteer,status=1)

    closedNeeds = Needs.objects.filter(host=volunteer,status=2)

    volunteer_state = Volunteer.objects.get(host=request.user).state

    page = 'volunteer'

    context = {'pendingNeeds':pendingNeeds, 'activeNeeds': activeNeeds, 'closedNeeds':closedNeeds, 'volunteer_state':volunteer_state, 'page':page}

    if request.method == 'POST':
        
        requirements = request.POST.get('requirements')
        volunteer = Volunteer.objects.get(host=request.user)
        state = volunteer.state

        print(state)
        
        state_committee = StateCommittee.objects.filter(state=state).first()

        print(state_committee)

        Needs.objects.create(host=volunteer,state_committee=state_committee, requirements=requirements)

        return redirect('volunteer-home')

    return render(request, 'Front/volunteer.html', context)
def complaintsview(request):
    user = request.user
    
    complaint = Complaint.objects.filter(userid=user)
    return render(request,'Front/viewcomplaints.html',{'complaint':complaint})
def complaintsadd(request):
    if request.method == "POST":
        complaint=Complaint()
        complaint.compaint=request.POST.get('compaint')
        complaint.userid = request.user
        complaint.save()
        return redirect('/complaintsview')
    
     
    return render(request, 'Front/addcomplaint.html')
def editcomplaint(request,id):
    edit=Complaint.objects.get(id=id)
    if request.method == "POST" :
       
        edit.compaint=request.POST.get('compaint')
        
        edit.save()
        return redirect('/complaintsview')
    return render(request,'Front/editcomplaints.html',{'edit':edit})
def deletecomplaint(request,id):
    complaint=Complaint.objects.get(id=id)
    complaint.delete()
    return redirect('/complaintsview')


def estimateamount(request):
    if request.method == "POST":
        cost=EstimateCost()
        cost.amount=request.POST.get('amount')
        cost.userid=request.user
        cost.bill=request.POST.get('bill')
        
        if len(request.FILES) != 0:
            cost.bill=request.FILES['bill']
        cost.save()
        # estimate = request.FILES.get('estimate')
        return redirect('/volunteerhome')
    return render(request, 'Front/estimateamount.html')








# User home page
@login_required(login_url='login')
@userOnly 
def userHome(request):
    return render(request, 'Front/user/userhome.html')







# CHANGE STATUS OF NEEDS (UPDATE)

# VERIFY BY STATE
@login_required(login_url='login')
@adminStateOnly
def needsVerifyByState(request, pk):

    need = Needs.objects.get(id=pk)

    if request.user.user_type == 1:

       need.is_verified_by_state = 1
    
    if request.user.user_type == 0 :

        need.is_verified_by_admin = 1
        need.status = 1

    need.save()

    return redirect ('needs')

# REJECT BY STATE
@login_required(login_url='login')
@adminStateOnly
def needsRejectByState(request, pk):
    
    need = Needs.objects.get(id=pk)

    if request.user.user_type == 1:

      need.is_verified_by_state = 2
      need.status = 2
      need.rejected_by = 1

    if request.user.user_type == 0:

        need.is_verified_by_admin =2
        need.status =2
        need.rejected_by = 0

    need.save()

    return redirect('needs')


# CLOSE NEEDS
@login_required(login_url='login')
@adminStateVolunteerOnly
def closeNeeds(request, pk):
    
    if request.user.user_type == 0 :
        need = Needs.objects.get(id=pk)

        need.status = 2
        need.rejected_by= 0

        need.save()

        return redirect('needs')

    elif request.user.user_type == 1 :

        need = Needs.objects.get(id=pk)
        need.status = 2
        need.rejected_by = 1
        need.save()

        return redirect('needs')

    elif request.user.user_type == 2 :

        need = Needs.objects.get(id=pk)
        need.status = 2
        need.rejected_by = 2
        need.save()

        return redirect('volunteer-home')
    
    else:
        return redirect('user-home')

    
    
@login_required(login_url='login')
@adminStateVolunteerOnly
def deleteNeeds(request,pk):
    need = Needs.objects.get(id=pk)
    need.delete()

    if request.user.user_type == 0 or request.user.user_type == 1:
        return redirect('needs')
    elif request.user.user_type ==2 :
        return redirect('volunteer-home')
    else:
        return redirect('user-home')
   
    
@login_required(login_url='login')
@userOnly
def userRequestPage(request):

    endUser = EndUser.objects.get(host=request.user)

    pendingAlerts = Alert.objects.filter(host=endUser,status=0)

    activeAlerts = Alert.objects.filter(host=endUser,status=1)

    closedAlerts = Alert.objects.filter(host=endUser,status=2)
    
    endUser_state = endUser.state

    context = {'pendingAlerts':pendingAlerts, 'activeAlerts':activeAlerts, 'closedAlerts':closedAlerts, 'endUser_state':endUser_state}



    if request.method == 'POST':
       
       content = request.POST.get('alertcontent') 
       endUser = EndUser.objects.get(host=request.user)
       state = endUser.state
       state_committee = StateCommittee.objects.filter(state=state).first()

       Alert.objects.create(host=endUser, content=content,status=0,
                             state_committee=state_committee
                            )

       return redirect('user-home')


    return render(request, 'Front/User/userRequest.html', context)



# Verify Alert


@login_required(login_url='login')
@adminStateOnly
def verifyAlert(request,pk):
    alert = Alert.objects.get(id=pk)

    if request.user.user_type == 1:

       alert.is_verified_by_state = 1
    
    if request.user.user_type == 0 :

        alert.is_verified_by_admin = 1
        alert.status = 1

    alert.save()

    return redirect ('alerts')



#Reject Alert

@login_required(login_url='login')
@adminStateOnly
def rejectAlert(request,pk):
    
    alert = Alert.objects.get(id=pk)

    if request.user.user_type == 1:

      alert.is_verified_by_state = 2
      alert.status = 2
      alert.rejected_by = 1

    if request.user.user_type == 0:

        alert.is_verified_by_admin =2
        alert.status =2
        alert.rejected_by = 0

    alert.save()

    return redirect('alerts')


# Delete Alert
@login_required(login_url='login')
@adminStateUserOnly
def deleteAlert(request, pk):
    alert = Alert.objects.get(id=pk)
    alert.delete()

    if request.user.user_type == 0 or request.user.user_type == 1:
        return redirect('alerts')
    elif request.user.user_type ==2 :
        return redirect('volunteer-home')
    else:
        return redirect('user-home')
    

@login_required(login_url='login')
@adminStateUserOnly
def closeAlert(request, pk):
    
    if request.user.user_type == 0 :
        alert = Alert.objects.get(id=pk)

        alert.status = 2
        alert.rejected_by= 0

        alert.save()

        return redirect('alerts')

    elif request.user.user_type == 1 :

        alert = Alert.objects.get(id=pk)
        alert.status = 2
        alert.rejected_by = 1
        alert.save()

        return redirect('alerts')

    elif request.user.user_type == 3 :

        alert = Alert.objects.get(id=pk)
        alert.status = 2
        alert.rejected_by = 2
        alert.save()

        return redirect('user-home')
    
    else:
        return redirect('volunteer-home')


def mapAlert(request,pk):
    user = User.objects.get(id=pk)
    volunteer = Volunteer.objects.get(host=user)
    volunteer_state = volunteer.state
    state_committee = StateCommittee.objects.filter(state=volunteer_state).first()
    alerts = Alert.objects.filter(state_committee=state_committee).exclude(status=2).first()

    context = {'alerts': alerts}

    return render(request, 'Front/mapAlert.html', context)
def unknownAlert(request):  
    alerts = Alert.objects.filter(latitude__isnull=False) 
    context = {'alerts': alerts}  
    return render(request, 'Front/mapunknown.html', context)


def viewReports(request):
    open_alerts = Alert.objects.filter(status=1)
    close_alerts = Alert.objects.filter(status=2)
    open_needs = Needs.objects.filter(status=1)
    close_needs = Needs.objects.filter(status=2)
    context = {'open_alerts':open_alerts,
               'close_alerts':close_alerts,
              'open_needs':open_needs,
               'close_needs':close_needs
               } 
    return render(request, 'base/reports/reports.html',context)

@login_required(login_url='login')
def requestCertificate(request):
    volunteer = Volunteer.objects.get(host=request.user)
    nonNeeds = Needs.objects.filter(host=volunteer, cr_status=0, status=2)
    certificates = Certificate.objects.filter(volunteer=volunteer)
    print(certificates)
    context = {'nonNeeds':nonNeeds, 'certificates':certificates}

    return  render(request, 'Front/certificate.html', context)

@login_required(login_url='login')
def submitCertificate(request, pk):
    if request.method == 'POST':
      amount =  request.POST.get('amount')
      estimate = request.FILES.get('estimate')
      need = Needs.objects.get(id=pk)
      volunteer = Volunteer.objects.get(host=request.user)
      Certificate.objects.create(volunteer=volunteer, need=need, amount=amount, estimate=estimate)
      need.cr_status = 1
      need.save()

      return redirect('request-certificate')
    

@login_required(login_url='login')    
def viewCerficates(request):
    pending_certificates = Certificate.objects.filter(status=0)
    recent_certificates = Certificate.objects.exclude(status=0)
    

    context = {'pending_certificates':pending_certificates,'recent_certificates':recent_certificates }

    

    return render(request, 'base/certificates/certificate.html', context)

@login_required(login_url='login')
@adminOnly
def approveCertificate(request, pk):
    certificate = Certificate.objects.get(id=pk)
    certificate.status = 1
    certificate.save()
    return redirect('view-certificate')


@login_required(login_url='login')
@adminOnly
def rejectCertificate(request, pk):
    certificate = Certificate.objects.get(id=pk)
    certificate.status = 2
    certificate.save()
    return redirect('view-certificate') 


@login_required(login_url='login')
def fullCertificate(request, pk):
    certificate = Certificate.objects.get(id=pk)
    context = {'certificate': certificate}
    return render(request,'Front/certificateFull.html', context)




def weatherReport(request):
    return render(request,'Front/weatherreport.html')

def hotspotView(request):
    alerts = Alert.objects.all()
    hotspot_coordinates = []

    for alert in alerts:
        if(alert.host):
            latitude = alert.host.latitude
            longitude = alert.host.longitude
            hotspot_coordinates.append({'latitude': latitude, 'longitude': longitude})

    context = {'hotspot_coordinates': hotspot_coordinates}
    return render(request, 'Front/hotspot.html', context)

import json
def save_alert(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        print(data) 
        alert = Alert.objects.create(latitude=latitude, longitude=longitude)
         
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
def viewTask(request,id):
    task = get_object_or_404(Task_voluenteer, id=id) 
    if task.alertid.host!=None:
        latitude = task.alertid.host.latitude
        longitude = task.alertid.host.longitude
    else:
        latitude = task.alertid.latitude
        longitude = task.alertid.longitude
        
    cordinates = {'latitude':latitude,'longitude':longitude}
    return render(request,'Front/viewtask.html',{'coordinates':cordinates})


def viewAllAlerts(request):
    task = get_object_or_404(Task_voluenteer, id=4)
    latitude = task.alertid.host.latitude
    longitude = task.alertid.host.longitude
    alerts = Alert.objects.exclude(status=2) 
    return render(request,'Front/viewallalerts.html',{'alerts':alerts})
from django.http import HttpResponse
# from reportlab.lib.pagesizes import portrait
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.units import inch
# import uuid
# from datetime import date
# def generate_pdf(request):
#     # Define custom dimensions for certificate size
    
#     username = request.user.name
#     certificate_width = 8.5 * inch
#     certificate_height = 11 * inch

#     # Create a response object
#     response = HttpResponse(content_type='application/pdf')
#     # Set the filename for the PDF
#     response['Content-Disposition'] = 'attachment; filename="disaster_certificate.pdf"'

#     # Create a PDF document with custom dimensions
#     doc = SimpleDocTemplate(response, pagesize=(certificate_width, certificate_height), rightMargin=0, leftMargin=0, topMargin=0, bottomMargin=0)

#     # Styles for the certificate
#     styles = getSampleStyleSheet()
#     style_title = styles["Title"]
#     style_body = styles["BodyText"]

#     # Define content for the PDF
#     content = []

#     # Title
#     title_text = "Certificate of Disaster Proof Approval"
#     title = Paragraph(title_text, style_title)
#     content.append(title)

#     # Add space
#     content.append(Spacer(1, 0.5 * inch))

#     # Acknowledgement paragraph 1
#     ack_text1 = f"We hereby acknowledge the occurrence of a disaster in the region of Mr./Ms. {username} and confirm that appropriate measures have been taken to mitigate its effects."
#     ack_paragraph1 = Paragraph(ack_text1, style_body)
#     content.append(ack_paragraph1)

#     # Add space
#     content.append(Spacer(1, 0.2 * inch))

#     # Acknowledgement paragraph 2
#     ack_text2 = "We appreciate your cooperation and understanding during this challenging time."
#     ack_paragraph2 = Paragraph(ack_text2, style_body)
#     content.append(ack_paragraph2)

#     # Add space
#     content.append(Spacer(1, 0.5 * inch))
#     today_date = date.today().strftime("%Y-%m-%d")  # Get today's date in YYYY-MM-DD format

#     # Approval details
#     approval_details = [
#         ("Approval ID", str(uuid.uuid4().hex)[:8]),
#         ("Date", today_date),
#         ("Approved by", "National Disaster Committee"), 
#         ("Approval Status", "Approved")
#     ]

#     # Convert approval details to table format
#     approval_table_data = [[Paragraph(label, style_body), Paragraph(value, style_body)] for label, value in approval_details]
#     approval_table = Table(approval_table_data)

#     # Add approval table to content
#     content.append(approval_table)

#     # Add space
#     content.append(Spacer(1, 0.5 * inch))

#     # Insert the image and align to the right
#     image_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Government_of_India_logo.svg/2560px-Government_of_India_logo.svg.png"
#     img = Image(image_path, width=2*inch, height=2*inch)
#     img.hAlign = 'RIGHT'
#     content.append(img)

#     # Build the PDF document
#     doc.build(content)

#     return response
@login_required(login_url='login')
@adminOnly
def viewestimateamount(request):
    data = EstimateCost.objects.all()
    return render(request,'base/alerts/viewestimation.html',{'data':data})
def approve_estimate(request, estimate_id):
    estimate = get_object_or_404(EstimateCost, id=estimate_id)
    estimate.status = 1  # Assuming 1 represents approved status
    estimate.save()
    return redirect('/viewestimateamount')
def reject_estimate(request, estimate_id):
    estimate = get_object_or_404(EstimateCost, id=estimate_id)
    estimate.status = 2  # Assuming 2 represents rejected status
    estimate.save()
    return redirect('/viewestimateamount') 
@login_required(login_url='login')
@userOnly
def claimuser(request):
    if request.method == "POST":
        cost=UserClaim()
        cost.claimname=request.POST.get('claimname')
        cost.address=request.POST.get('address')
        cost.claimtype=request.POST.get('claimtype')
        cost.description=request.POST.get('description')
        
        cost.userid=request.user
        cost.image=request.POST.get('image')
        
        if len(request.FILES) != 0:
            cost.image=request.FILES['image']
        cost.save()
        # estimate = request.FILES.get('estimate')
        return redirect('/claimuser')
    return render(request,'Front/User/addclaim.html')
@login_required(login_url='login')
@adminOnly
def viewclimuseradmin(request):
    data = UserClaim.objects.all()
    print("data ",data)
    return render(request,'base/alerts/viewclimuseradmin.html',{'data':data})

def viewcomplaintsbyadmin(request):
    data = Complaint.objects.all()
    return render(request,'base/alerts/viewcomplaints.html',{'data':data}) 

@login_required(login_url='login')
@volunteerOnly

def viewtaskebystate(request):
    user = request.user.id
    volunteer = Volunteer.objects.filter(host=user).first()
    print("datas:",volunteer)
    tasks = Task_voluenteer.objects.filter(volunteerid=volunteer.id)
     
    return render(request,'base/volunteer/viewtasks.html',{'tasks':tasks})