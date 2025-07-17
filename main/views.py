from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import FoodItem, Category
from .forms import FoodItemForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def inventory_list(request):
    query = request.GET.get('q', '')
    items = FoodItem.objects.all()

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(storage_location__icontains=query)
        )

    items = items.order_by('name')  # Keep alphabetized

    unit_choices = FoodItem._meta.get_field('unit').choices
    storage_choices = FoodItem._meta.get_field('storage_location').choices

    return render(request, 'main/inventory_list.html', {
        'items': items,
        'unit_choices': unit_choices,
        'storage_choices': storage_choices,
        'query': query,
    })
def add_food_item(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = FoodItemForm()
        recent_items = FoodItem.objects.order_by('-id').values_list('name', flat=True).distinct()[:10]

    return render(request, 'main/add_food_item.html', {
        'form': form,
        'recent_foods': list(recent_items),
        })        
    
def delete_food_item(request, item_id):
        item = FoodItem.objects.get(id=item_id)
        item.delete()
        return redirect('inventory_list')
    
@csrf_exempt
def update_food_item(request, item_id):
    if request.method == 'POST':
        item = FoodItem.objects.get(id=item_id)
        field = request.POST.get('field')
        value = request.POST.get('value')
        
        if field in ['name', 'quantity', 'unit', 'storage_location', 'expiration_date']:
            setattr(item, field, value)
            item.save()
            return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)    


def food_name_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = list(
        FoodItem.objects
        .filter(name__icontains=query)
        .values_list('name', flat=True)
        .distinct()[:10]
    )
    return JsonResponse({'suggestions': suggestions})
