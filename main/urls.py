from django.urls import path

from .views import inventory_list, add_food_item, delete_food_item, food_name_suggestions, todo_list, add_todo,toggle_complete, delete_todo, update_todo

urlpatterns = [
    path("", inventory_list, name="inventory_list"),
    path("add/", add_food_item, name="add_food_item"),
    path("delete/<int:item_id>/", delete_food_item, name='delete_food_item'),
    path('ajax/food-suggestions/', food_name_suggestions, name='food_name_suggestions'),
    path('', todo_list, name='todo_list'),
    path('add-todo/', add_todo, name='add_todo'),
    path('toggle/<int:pk>/', toggle_complete, name='toggle_complete'),



]