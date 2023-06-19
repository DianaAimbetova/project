from curses.ascii import isascii
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Contact
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

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
   actions = Action.objects.exclude(user=request.user)
   following_ids = request.user.following.values_list('id',
   flat=True)
   if following_ids:
      # If user is following others, retrieve only their actions
      actions = actions.filter(user_id__in=following_ids)
   actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
   return render(request, 'account/dashboard.html',
                 {'section': 'dashboard',
                  'actions': actions})

def register(request):
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
          user = form.save(commit=False)
          user.set_password(form.cleaned_data['password'])
          user.save()
          Profile.objects.create(user = user)
          create_action(user, 'has created an account')
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

@login_required
def user_list(request):
   current_user = request.user
   users = User.objects.filter(is_active = True).exclude(pk=current_user.id)
   return render(request, 'account/list.html', {'section': 'people',
                                                     'users': users})

@login_required
def user_detail(request, username):
   user = get_object_or_404(User, username=username, is_active=True)
   return render(request, 'account/detail.html',{'section': 'people',
                                                      'user': user})

@require_POST
@login_required
def user_follow(request):
   user_id = request.POST.get('id')
   action = request.POST.get('action')
   if user_id and action:
      try:
         followed_user = User.objects.get(id=user_id)
         following_user = request.user
         if action == 'follow':
            Contact.objects.get_or_create(user_from=following_user, user_to=followed_user)
            create_action(following_user, 'is following', followed_user)
         else:
            Contact.objects.filter(user_from=following_user, user_to=followed_user).delete()
         return JsonResponse({'status':'ok'})
      except  User.DoesNotExist:
         return JsonResponse({'status':'error'})
   return JsonResponse({'status':'error'})

