from django.urls import path
from .views import InventoryManagementView

urlpatterns = [
    path("items/", InventoryManagementView.as_view(), name="item-view"),
    path("items/<int:item_id>/", InventoryManagementView.as_view(), name="item-view-get"),
]