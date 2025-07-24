from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import FoodItem, Category, Todo
from .forms import FoodItemForm, TodoForm
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

    # ✅ Todo & Grocery List additions
    todos = Todo.objects.filter(list_type='lori').order_by('-created_at')
    groceries = Todo.objects.filter(list_type='grocery').order_by('-created_at')
    form = TodoForm(initial={'list_type': 'lori'})
    grocery_form = TodoForm(initial={'list_type': 'grocery'})

    return render(request, 'main/inventory_list.html', {
        'items': items,
        'unit_choices': unit_choices,
        'storage_choices': storage_choices,
        'query': query,
        'form': form,
        'grocery_form': grocery_form,
        'todos': todos,
        'groceries': groceries,
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

def todo_list(request):
    form = TodoForm()
    todos = Todo.objects.all().order_by('-created_at')
    return render(request, 'todo_list.html', {'todos': todos, 'form': form})

def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('inventory_list')

@csrf_exempt
def toggle_complete(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        todo.completed = not todo.completed
        todo.save()
        return JsonResponse({'success': True, 'completed': todo.completed})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        todo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def update_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, pk=pk)
        title = request.POST.get('title', '').strip()
        if title:
            todo.title = title
            todo.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

def add_grocery(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data['list_type'] = 'grocery'  # Force the type regardless of form input
        form = TodoForm(data)
        if form.is_valid():
            form.save()
    return redirect('inventory_list')

@csrf_exempt
def toggle_grocery(request, id):
    todo = get_object_or_404(Todo, id=id, list_type='grocery')
    todo.completed = not todo.completed
    todo.save()
    return JsonResponse({'success': True, 'completed': todo.completed})

@csrf_exempt
def update_grocery(request, id):
    todo = get_object_or_404(Todo, id=id, list_type='grocery')
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title)
        todo.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_grocery(request, id):
    todo = get_object_or_404(Todo, id=id, list_type='grocery')
    todo.delete()
    return JsonResponse({'success': True})