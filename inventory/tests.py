from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import InventoryItem
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class InventoryManagementTests(TestCase):
    def setUp(self):
        """Set up test client, test user, and test data."""
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Generate a JWT token for the test user
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        # Authenticate client with JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Test data
        self.item_data = {"name": "Test Item", "description": "Test Description"}
        self.item = InventoryItem.objects.create(**self.item_data)
        self.item_url = f"/items/{self.item.id}/"
        self.create_url = "/items/"

    def test_create_item_success(self):
        """Test creating an inventory item successfully."""
        new_item = {"name": "New Item", "description": "New Description"}
        response = self.client.post(self.create_url, new_item, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], new_item["name"])

    def test_create_item_duplicate(self):
        """Test creating a duplicate inventory item."""
        response = self.client.post(self.create_url, self.item_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_item_success(self):
        """Test retrieving an existing inventory item."""
        response = self.client.get(self.item_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.item.name)

    def test_get_item_not_found(self):
        """Test retrieving a non-existing inventory item."""
        response = self.client.get("/items/9999/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_update_item_success(self):
        """Test updating an existing inventory item."""
        updated_data = {"name": "Updated Item"}
        response = self.client.put(self.item_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], updated_data["name"])

    def test_update_item_not_found(self):
        """Test updating a non-existing inventory item."""
        response = self.client.put("/items/9999/", {"name": "Not Found"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_delete_item_success(self):
        """Test deleting an existing inventory item."""
        response = self.client.delete(self.item_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_delete_item_not_found(self):
        """Test deleting a non-existing inventory item."""
        response = self.client.delete("/items/9999/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
