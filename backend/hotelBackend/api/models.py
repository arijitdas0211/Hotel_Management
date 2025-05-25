from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# from django.forms import ValidationError

USER_TYPES = [
    ('superuser', 'SuperUser'),
    ('staff', 'Staff'),
    ('customer', 'Customer')
]

FOOD_CHOICES = [
    (1, "Veg"),
    (2, "Non-Veg"),
    (3, "Both")
]

class MyUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    
    class Meta:
        db_table = 'myUser'


class SuperUserProfile(models.Model):
    super_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex=r'^\d{10}$')])
    created_at = models.DateTimeField(auto_now_add=True)
    myUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'superuser'

    def __str__(self):
        return f"{self.myUser.get_full_name()}"


class StaffType(models.Model):
    id = models.AutoField(primary_key=True)
    staffType = models.CharField(max_length=100)
    created_by = models.ForeignKey(SuperUserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_type'
        verbose_name = 'Staff Type'
        verbose_name_plural = 'Staff Types'

    def __str__(self):
        return self.staffType


class StaffProfile(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex=r'^\d{10}$')])
    staffType = models.ForeignKey(StaffType, on_delete=models.CASCADE)
    myUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_by = models.ForeignKey(SuperUserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.myUser.get_full_name()}"


class CustomerProfile(models.Model):
    cust_id = models.AutoField(primary_key=True)
    foodPref = models.IntegerField(choices=FOOD_CHOICES, default=3)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex=r'^\d{10}$')])
    created_at = models.DateTimeField(auto_now_add=True)
    myUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return f"{self.myUser.get_full_name()}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    tableNo = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, default='free', choices=[('free', 'Free'), ('reserved', 'Reserved')])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(SuperUserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'table'

    def __str__(self):
        return f"Table {self.tableNo}"


class FoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    food_type = models.IntegerField(choices=FOOD_CHOICES, default=3)
    status = models.BooleanField(default=True, choices=[(True, 'Enabled'), (False, 'Disabled')])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(SuperUserProfile, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        db_table = 'food_category'

    def __str__(self):
        return self.category_name


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    food_type = models.IntegerField(choices=FOOD_CHOICES, default=3)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, choices=[(True, 'Enabled'), (False, 'Disabled')])
    created_by = models.ForeignKey(SuperUserProfile, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return self.name


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    totalPeople = models.PositiveIntegerField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, default=None)
    food_type = models.IntegerField(choices=FOOD_CHOICES, default=3)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    # assigned_to = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='confirmed', choices=[
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('progress', 'Progress'),
        ('completed', 'Completed')
    ])

    class Meta:
        db_table = 'booking'
        ordering = ['-booking_time']

    def __str__(self):
        return f"Booking {self.id}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Menu, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='progress', choices=[('progress', 'Progress'), ('completed', 'Completed')])
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order: {self.id} | {self.booking.customer.first_name}"


class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    billItems = models.ForeignKey(Order, on_delete=models.CASCADE)
    totalAmount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    paymentStatus = models.BooleanField(default=False)
    paymentMode = models.CharField(max_length=100, choices=[
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI')
    ], default='cash')
    created_by = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'billing'
        ordering = ['-created_at']

    def __str__(self):
        return f"Billing {self.id}"


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback_status = models.BooleanField(default=False)
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'feedback'
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback {self.id}"
