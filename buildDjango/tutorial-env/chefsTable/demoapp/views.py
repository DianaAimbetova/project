from django.shortcuts import render
from django.http import HttpResponse
from .forms import ApplicationForm  
from .forms import BookingForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .models import MyMenu

# Create your views here.
def home(request):
    return render(request, "index.html")

'''def index(request):  
    path = request.path  
    method = request.method  
    body = request.body
    content='''  
''''<center><h2>Testing Django Request Response Objects</h2>  
<p>Request path : " {}</p>  
<p>Request Method :{}</p>
<p>Request Body :{}</p></center>  '''
'''.format(path, method, body)  
    return HttpResponse(content)'''

def showform(request):  
    return render(request, "form.html")

def getform(request):  
    if request.method == "POST":  
        id=request.POST['id']  
        name=request.POST['name']  
    return HttpResponse("Name:{} UserID:{}".format(name, id))

def menuitems(request, dish):
    items = {'pasta': 'Pasta is delicious',
             'falafel' : 'Falfel is delicious',
             'cheesecake' : 'Cheesecake is delicious'}
    
    description = items[dish]
    return HttpResponse(f"<h2>{dish}</h2>" + description)

 
def index(request):  
    form = ApplicationForm()  
 
    return render(request, 'form.html', {'form': form})
 
def form_view(request): 
    form = BookingForm() 
    if request.method == 'POST': 
        form = BookingForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            context = {"form" : form} 
            return render(request, "booking.html", context)
        
def myview(request):
    if request.user.is_anonymous():
        raise PermissionDenied()
    else:
        return HttpResponse(f'Hello, ',request.user)

@login_required    
def newmyview(request):
    return HttpResponse(f'Hello, ',request.user)

def about(request):    
    return render(request, "about.html")

def menu(request):
    menuitem = {'mains': [
        {'name' : "Falafel", 'price' : 12},
        {'name' : "Shawarma", 'price' : 15},
        {'name' : "Gyro", 'price' : 10},
        {'name' : "Hummus", 'price' : 5},
                          ]}
    return render(request, 'menu.html', menuitem)

def menu_by_id(request):
    newmenu = MyMenu.objects.all()
    newmenu_dict = {'menu' : newmenu}
    return render(request, 'menu_card.html', newmenu_dict)