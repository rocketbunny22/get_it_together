from django import forms
from .models import FoodItem
from .models import Todo


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'category', 'quantity', 'unit', 'storage_location', 'expiration_date']
        
    expiration_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Add a new task...'})
        }    