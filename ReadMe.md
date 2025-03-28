# Inventory Management System API 🚀

## Overview  

This project is a **backend API** for a simple **Inventory Management System**, built using **Django Rest Framework (DRF)**. It supports **CRUD operations** for managing inventory items and includes **JWT authentication, Redis caching, logging, and unit testing** to ensure security and performance.

---

## Features 🔥  

### ✅ **Authentication & Security**  
- **JWT Authentication** for securing API endpoints.  
- Users must be authenticated to access inventory operations.  

### ✅ **CRUD Operations for Inventory Items**  
- **Create:** Add a new inventory item.  
- **Read:** Retrieve item details.  
- **Update:** Modify existing inventory items.  
- **Delete:** Remove an item from inventory.  

### ✅ **Redis Caching** 🏎️  
- **Frequent item retrievals** are cached to boost performance.  
- Uses **Redis** to store accessed items for faster response.  

### ✅ **Database Management** 🗃️  
- **PostgreSQL** for storing inventory data.  
- Uses **Django ORM** for efficient database interactions.  

### ✅ **Logging & Monitoring** 📜  
- Integrated **logging system** to track API requests, errors, and debugging info.  
- Uses different **logging levels** (INFO, DEBUG, ERROR).  

### ✅ **Unit Testing** 🛠️  
- Comprehensive **unit tests** using Django’s test framework.  
- Ensures API stability and correctness.  

---

## Technology Stack 🏗️  

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL  
- **Caching:** Redis  
- **Authentication:** JWT (JSON Web Token)  
- **Testing:** Django Test Framework  
- **Logging:** Python’s Logging Module  

---

## API Endpoints 🚀  

### 🔐 **Authentication**  
| Method | Endpoint       | Description |
|--------|--------------|------------|
| POST   | `/auth/register/` | User Registration |
| POST   | `/auth/login/` | User Login (Get JWT Token) |
| POST   | `/auth/refresh/` | Refresh JWT Token |

### 📦 **Inventory Management**  
| Method | Endpoint           | Description |
|--------|----------------|------------|
| POST   | `/items/` | Create a new inventory item |
| GET    | `/items/{item_id}/` | Retrieve details of an item (Uses Redis caching) |
| PUT    | `/items/{item_id}/` | Update an item |
| DELETE | `/items/{item_id}/` | Delete an item |

---

## Installation & Setup 🚀  

### 1️⃣ **Clone the Repository**  
```sh
git clone https://github.com/hasanpp/InventoryApi.git
cd inventory-api
python -m venv venv
source venv/bin/activate 
