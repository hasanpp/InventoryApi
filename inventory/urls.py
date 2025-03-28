from django.urls import path
from .views import InventoryManagementView
from django.http import HttpResponse


def home(request):
    return HttpResponse("This is the inventory API")

urlpatterns = [
    path("items/", InventoryManagementView.as_view(), name="item-view"),
    path("items/<int:item_id>/", InventoryManagementView.as_view(), name="item-view-get"),
    path('', home, name='home'),
]