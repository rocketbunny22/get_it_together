from django.urls import path

from .views import inventory_list, add_food_item, delete_food_item, food_name_suggestions

urlpatterns = [
    path("", inventory_list, name="inventory_list"),
    path("add/", add_food_item, name="add_food_item"),
    path("delete/<int:item_id>/", delete_food_item, name='delete_food_item'),
    path('ajax/food-suggestions/', food_name_suggestions, name='food_name_suggestions')

]