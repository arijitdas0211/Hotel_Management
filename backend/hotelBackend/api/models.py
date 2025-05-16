from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError

# Create your models here.
"""
Inherited fields from Abstract User (User model):-
first_name,
last_name,
email,
username,
password,
last_login,
is_staff,
is_superuser,
is_active,
date_joined
"""
class MyUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    USER_TYPES = [
        ('superuser', 'SuperUser'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    ]
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    

class BaseProfile(models.Model):
    phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex=r'^\d{10}$')])
    createdAt = models.DateTimeField(auto_now_add=True)
    myUser = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
    

class SuperUser(BaseProfile):
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'superuser'
        
    def clean(self):
        if self.myUser.user_type != 'superuser':
            raise ValidationError("User must be of type 'superuser' to create Superuser profile.")

    def __str__(self):
        return f"{self.myUser.get_full_name() if self.myUser else 'unknown'} - {self.myUser.user_type}"


class StaffType(models.Model):
    id = models.AutoField(primary_key=True)
    staffType = models.CharField(max_length=100)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="stafftype_created_by_superuser")

    class Meta:
        db_table = 'staff_type'

    def __str__(self):
        return f"{self.staffType} - {self.created_by.get_full_name() if self.created_by else 'unknown'}" 
    

class Staff(BaseProfile):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="staff_created_by_superuser")

    class Meta:
        db_table = 'staff'
        
    def clean(self):
        if self.myUser.user_type != 'staff':
            raise ValidationError("User must be of type 'staff' to create Staff profile.")

    def __str__(self):
        return f"{self.created_by} - {self.myUser.get_full_name()}"


FOOD_CHOICES = [
    (1, "Veg"),
    (2, "Non-Veg"),
    (3, "Both")
]

class Customer(BaseProfile):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200)
    foodPref = models.IntegerField(choices = FOOD_CHOICES, default=3)

    class Meta:
        db_table = 'customer'
        
    def clean(self):
        if self.myUser.user_type != 'customer':
            raise ValidationError("User must be of type 'customer' to create Customer profile.")

    def __str__(self):
        return f"{self.myUser.get_full_name() if self.myUser else 'unknown'} - {self.myUser.user_type}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    tableNo = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Inactive')])
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="table_created_by_superuser_or_staff")

    class Meta:
        db_table = 'table'

    def __str__(self):
        return f"{self.tableNo} - {self.capacity} - {self.created_by.get_full_name() if self.created_by else 'unknown'}"
    

class FoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    food_type = models.IntegerField(choices = FOOD_CHOICES, default=3)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="food_category_created_by_superuser_or_staff")

    class Meta:
        db_table = 'food_category'

    def __str__(self):
        return f"{self.category_name} - {self.created_by.get_full_name() if self.created_by else 'unknown'}"


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    food_type = models.IntegerField(choices = FOOD_CHOICES, default=3)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Inactive')])
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="menu_created_by_superuser_or_staff")

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return f"{self.name} - {self.food_type} - {self.food_category} - {self.created_by.get_full_name() if self.created_by else 'unknown'}"


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    bookingDateTime = models.DateTimeField(auto_now_add=True)
    totalPeople = models.PositiveIntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    customer = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="booking_for_customer_name")
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="booking_created_by_customer_or_staff")
    assigned_to = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="assigned_to_staff_name")
    status = models.CharField(max_length=20, default='confirmed', choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('progress', 'Progress')])

    class Meta:
        db_table = 'booking'
        ordering = ['-bookingDateTime']

    def __str__(self):
        return f"{self.id} - {self.table.tableNo} - {self.customer.get_full_name() if self.customer else 'unknown'} - {self.created_by.get_full_name() if self.created_by else 'unknown'} - {self.bookingDateTime.date()} | {self.bookingDateTime.date()} - {self.assigned_to.get_full_name()}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Menu)
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, choices=[(True, 'Completed'), (False, 'In Progress')])
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="order_created_by_customer_or_staff")

    class Meta:
        db_table = 'order'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.id} - {self.booking.customer.get_full_name() if self.booking.customer else 'unknown'} - {self.created_by.get_full_name() if self.created_by else 'unknown'} - {self.booking.table.tableNo} - {self.createdAt.date()} - {self.createdAt.time()} - {self.status}"


class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    totalAmount = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, choices=[(True, 'Generated'), (False, 'Pending')])
    paymentStatus = models.BooleanField(default=False, choices=[(True, 'Paid'), (False, 'Unpaid')])
    paymentMode = models.CharField(max_length=100, choices=[('cash', 'Cash'), ('card', 'Card'), ('upi', 'UPI')], default='cash')
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.id} - {self.order.booking.customer.get_full_name() if self.order.booking.customer else 'unknown'} - {self.status} - {self.paymentStatus} - {self.order.booking.id} - {self.order.booking.table.tableNo}"


class Feedback(models.Model):
    id = models.AutoField(primary_key = True)
    rating = models.IntegerField(default=0, choices = [(i, str(i)) for i in range(1, 6)]) # 1 to 5 rating
    feedback = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    feedback_status = models.BooleanField(default = False, choices=[(True, 'Provided'), (False, 'Not Provided')])
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feedback'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.id} - {self.billing.order.booking.customer.get_full_name() if self.billing.order.booking.customer else 'unknown'} - {self.billing.id} - {self.rating} - {self.feedback_status} - {self.billing.order.booking.assigned_to.get_full_name() if self.billing.order.booking.assigned_to else 'unknown'}"

