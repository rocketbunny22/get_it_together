from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class FoodItem(models.Model):
        name = models.CharField(max_length=100, unique=True)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        quantity = models.FloatField()
        unit = models.CharField(max_length=50, choices=[('pcs', 'Pieces'), ('lbs', 'Pounds'), ('oz', 'Ounces')])
        storage_location = models.CharField(max_length=100, choices=[('fridge', 'Fridge'), ('basement', 'Basement'), ('hall_closet', 'Hall Closet')])
        expiration_date = models.DateField(null=True, blank=True)
        
        def __str__(self):
            return f"{self.name} ({self.quantity} {self.unit})"
        
        def is_expiring_soon(self):
            from datetime import date, timedelta
            return self.expiration_date and self.expiration_date <= date.today() + timedelta(days=3)
        
        def is_low_stock(self):
            return self.quantity <= 1       
        
class Todo(models.Model):
    LIST_CHOICES = [
        ('lori', "Lori's List"),
        ('grocery', 'Grocery List')
    ]
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    list_type = models.CharField(max_length=10, choices=LIST_CHOICES, default='lori')

    def __str__(self):
        return self.title
