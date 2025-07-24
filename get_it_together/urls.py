"""
URL configuration for get_it_together project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from main.views import add_grocery, update_food_item, delete_todo, update_todo, toggle_grocery, update_grocery, delete_grocery


urlpatterns = [
    path('admin/', admin.site.urls),
    path("main/", include("main.urls")),
    path('delete_todo/<int:pk>/', delete_todo, name='delete_todo'),
    path('update_todo/<int:pk>/', update_todo, name='update_todo'),
    path('add_grocery/', add_grocery, name='add_grocery'),
    path('grocery/toggle/<int:id>/', toggle_grocery, name='grocery_toggle'),
    path('grocery/update/<int:id>/', update_grocery, name='grocery_update'),
    path('grocery/delete/<int:id>/', delete_grocery, name='grocery_delete'),

    
]
