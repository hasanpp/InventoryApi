import logging
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.core.cache import cache
from .models import InventoryItem
from .serializers import InventoryItemSerializer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class InventoryManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        name = request.data.get("name")
        logger.info("POST request received to create an inventory item with name: %s", name)
        
        if InventoryItem.objects.filter(name=name).exists():
            logger.warning("Attempt to create an item that already exists: %s", name)
            return Response({"error": "Item already exists."}, status=400)
        
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Item created successfully: %s", serializer.data)
            return Response(serializer.data, status=201)
        logger.error("Failed to create item. Errors: %s", serializer.errors)
        return Response(serializer.errors, status=400)
       
    def get(self, request, item_id):
        logger.info("GET request received for item ID: %s", item_id)
        cache_key = f"inventory_item_{item_id}"
        cached_item = cache.get(cache_key)
        
        if cached_item:
            logger.info("Cache hit for item ID: %s", item_id)
            return Response(cached_item, status=200)
        
        try:
            item = InventoryItem.objects.get(id=item_id)
            serializer = InventoryItemSerializer(item)
            serialized_data = serializer.data
            cache.set(cache_key, serialized_data, timeout=3600)
            logger.info("Cache miss. Item retrieved and cached for ID: %s", item_id)
            return Response(serialized_data, status=200)
        except InventoryItem.DoesNotExist:
            logger.error("Item not found for ID: %s", item_id)
            return Response({"error": "Item not found."}, status=404)
     
    def put(self, request, item_id):
        logger.info("PUT request received to update item ID: %s", item_id)
        try:
            item = InventoryItem.objects.get(id=item_id)
        except InventoryItem.DoesNotExist:
            logger.error("Item not found for ID: %s", item_id)
            return Response({"error": "Item not found."}, status=404)
        
        serializer = InventoryItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            cache_key = f"inventory_item_{item_id}"
            cache.set(cache_key, serializer.data, timeout=3600)
            logger.info("Item updated successfully for ID: %s", item_id)
            return Response(serializer.data, status=200)
        logger.error("Failed to update item for ID: %s. Errors: %s", item_id, serializer.errors)
        return Response(serializer.errors, status=400)
     
    def delete(self, request, item_id):
        logger.info("DELETE request received for item ID: %s", item_id)
        try:
            item = InventoryItem.objects.get(id=item_id)
            item.delete()
            
            cache_key = f"inventory_item_{item_id}"
            cache.delete(cache_key)
            logger.info("Item deleted successfully for ID: %s", item_id)
            return Response({"message": "Item deleted successfully."}, status=200)
        except InventoryItem.DoesNotExist:
            logger.error("Item not found for ID: %s", item_id)
            return Response({"error": "Item not found."}, status=404)
