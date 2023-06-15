from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

# Create your views here.
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username = cd['username'],
#                                 password = cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()

#     return render(request, 'account/login.html', {'form': form})

# class MyLogin(LoginView):
#     redirect_authenticated_user = True
#     template_name = 'account/login.html'

#     def get_success_url(self):
#         return reverse_lazy('tasks') 
    
#     def form_invalid(self, form):
#         messages.error(self.request,'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))
    
# def tasks(request):
#     return HttpResponse(request, 'Hello World')


@login_required
def dashboard(request):
 return render(request,
 'account/dashboard.html',
 {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
          user = form.save(commit=False)
          user.set_password(form.cleaned_data['password'])
          user.save()
          Profile.objects.create(user = user)
          return render(request, 'account/register_done.html',{'new_user': user})
    else:
       form = UserRegistrationForm()
       return render(request,'account/register.html',{'form': form} )

@login_required    
def edit(request):
   if request.method == 'POST':
      user_form = UserEditForm(instance=request.user,
                               data = request.POST)
      profile_form = ProfileEditForm(instance=request.user.profile,
                                      data = request.POST,
                                      files=request.FILES)
      if user_form.is_valid() and profile_form.is_valid():
         user_form.save()
         profile_form.save()
         messages.success(request, 'Profile updated successfully')
      else:
         messages.error(request, 'Error updating your profile')
   else:
      user_form = UserEditForm(instance=request.user)
      profile_form = ProfileEditForm(instance=request.user.profile)
    
   return render(request, 'account/edit.html', {'user_form' : user_form,
                                             'profile_form' : profile_form})