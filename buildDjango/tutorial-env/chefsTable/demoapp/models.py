from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    menu_category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.menu_category_name

class MyMenu(models.Model):
    menu_item = models.CharField(max_length=200)
    price = models.IntegerField(null=False)
    category_id = models.ForeignKey(MenuCategory, on_delete=models.PROTECT, default=None, related_name='category_name')

    def __str__(self):
        return self.menu_item


class Booking(models.Model): 
    first_name = models.CharField(max_length = 200) 
    last_name = models.CharField(max_length = 200) 
    guest_count = models.IntegerField() 
    reservation_time = models.DateField(auto_now=True) 
    comments = models.CharField(max_length = 1000)

class Person(models.Model): 
    last_name = models.TextField() 
    first_name = models.TextField() 

    def __str__(self): 
        return f"{self.last_name}, {self.first_name}" 
    
class Employees(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    role = models.CharField(max_length=100)
    shift = models.IntegerField()


    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booking_time = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.first_name + " " + self.last_name
    
class Employee(models.Model):   
    name = models.CharField(max_length=100)   
    email = models.EmailField()   
    contact = models.CharField(max_length=15)   
    class Meta:   
        db_table = "Employee" 