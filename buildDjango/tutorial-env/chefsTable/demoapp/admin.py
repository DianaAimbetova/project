from django.contrib import admin
from .models import MyMenu, MenuCategory,Booking
from django.contrib.auth.models import User 
from django.contrib.auth.admin import UserAdmin
from .models import Person, Employees


# Register your models here.
admin.site.register(MyMenu)
admin.site.register(MenuCategory)
admin.site.register(Booking)
admin.site.register(Employees)


@admin.register(Person) 
class PersonAdmin(admin.ModelAdmin): 
    list_display = ("last_name", "first_name") 
    search_fields = ("first_name__startswith", ) 


# Unregister the provided model admin:  
admin.site.unregister(User)

@admin.register(User) 
class NewAdmin(UserAdmin): 
    readonly_fields = [ 
        'date_joined', 
    ] 

    def get_form(self, request, obj=None, **kwargs): 
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser 

        if not is_superuser: 
            form.base_fields['username'].disabled = True 

        return form   