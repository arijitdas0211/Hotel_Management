from django.db import models

# Create your models here.
class SuperUser(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Inactive')])
    is_superuser = models.BooleanField(default=True, choices=[(True, 'Superuser'), (False, 'Staff')])
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'superuser'

    def __str__(self):
        return self.name
    

class StaffType(models.Model):
    staff_type_id = models.AutoField(primary_key=True)
    staff_type_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(SuperUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff_type'

    def __str__(self):
        return self.staff_type_name 
    

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    staff_type = models.ForeignKey(StaffType, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True, choices=([True, 'Active'], [False, 'Inactive']))
    is_superuser = models.BooleanField(default=False, choices=([True, 'Super User'], [False, 'Staff']))
    superuser = models.ForeignKey(SuperUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff'

    def __str__(self):
        return f"{self.name} - {self.staff_type}"


food_choices = [
    (1, "Veg"),
    (2, "Non-Veg"),
    (3, "Both")
]

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    food_pref = models.IntegerField(choices = food_choices, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return self.name


class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_no = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.BooleanField(default=False, choices=[(True, 'Active'), (False, 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(SuperUser, on_delete=models.CASCADE)
    created_by = models.ForeignKey(Staff, on_delete=models.CASCADE)

    class Meta:
        db_table = 'table'

    def __str__(self):
        return str(self.table_no)
    

class FoodCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    food_type = models.IntegerField(choices = food_choices, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'food_category'

    def __str__(self):
        return f"{self.category_name} - {self.get_food_type_display()}"


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField()
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    food_type = models.IntegerField(choices = food_choices, default=3)
    item_status = models.BooleanField(default=True, choices=[(True, 'Active'), (False, 'Inactive')])
    item_image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Staff, on_delete=models.CASCADE)

    class Meta:
        db_table = 'menu'

    def __str__(self):
        return f"{self.item_name} - {self.get_food_type_display()} - {self.food_category.category_name}"


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    no_of_people = models.PositiveIntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    booking_status = models.BooleanField(default=False, choices=[(True, 'Confirmed'), (False, 'Cancelled')])

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f"{self.booking_id} - {self.customer.name} - {self.table.table_no} - {self.booking_date} - {self.booking_time}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False, choices=[(True, 'Completed'), (False, 'In Progress')])

    class Meta:
        db_table = 'order'

    def __str__(self):
        return f"{self.order_id} - {self.customer.name} - {self.table.table_no} - {self.order_date} - {self.order_time}"


class Billing(models.Model):
    bill_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    bill_date = models.DateField(auto_now_add=True)
    bill_time = models.TimeField(auto_now_add=True)
    bill_status = models.BooleanField(default=False, choices=[(True, 'Generated'), (False, 'Pending')])
    bill_payment_status = models.BooleanField(default=False, choices=[])

    class Meta:
        db_table = 'billing'

    def __str__(self):
        return str(self.bill_id)


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    billing = models.ForeignKey(Billing, on_delete = models.CASCADE)
    table = models.ForeignKey(Table, on_delete = models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0, choices = [(i, str(i)) for i in range(1, 6)]) # 1 to 5 rating
    feedback = models.TextField()
    feedback_date = models.DateField()
    feedback_time = models.TimeField()
    feedback_status = models.BooleanField(default = False, choices=[(True, 'Provided'), (False, 'Not Provided')])

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"{self.feedback_id} - {self.customer.name} - {self.billing.bill_date} - {self.rating} - {self.feedback_status}"


