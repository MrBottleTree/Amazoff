# Amazoff - E-commerce Platform

**Amazoff** is a simplified e-commerce platform (almost Amazon) built using **Django** and **SQL**, designed to facilitate buyers and sellers to manage inventories, place orders, track transactions, and leave reviews.

---

## Features

### User Management
- Two types of users: **Buyers & Sellers**
- User authentication and registration
- Profile management with wallet balance tracking

### E-commerce Functionality
- **Product Listings**: Sellers can add products with images, descriptions, and categories.
- **Inventory Management**: Sellers maintain stock at different addresses.
- **Shopping Cart**: Buyers can add items to their cart before checkout.
- **Order Placement**: Buyers place orders with multiple items from different sellers.

### Order & Fulfillment
- Orders contain **multiple order details** (each linked to a product & seller).
- Order statuses: **Pending, Accepted, Rejected**
- Each **order detail** tracks an individual product’s fulfillment status.
- **Order history page** displaying previous orders.

### Reviews & Ratings
- Buyers can leave reviews **only for accepted orders**.
- Buyers can **change their review** if they’ve already reviewed a product.

### Notifications
- Real-time order status updates via notifications.
- Sellers receive order fulfillment requests.

---

## Tech Stack
- **Backend:** Django (Python), SQLite/PostgreSQL
- **Frontend:** HTML, CSS, JavaScript (Bootstrap)
- **Deployment:** Cloudflare (for domain), PythonAnywhere/DigitalOcean

---

## Database Models
- **User (People):** Manages buyers & sellers.
- **Product:** Stores product details.
- **Inventory:** Tracks stock at different locations.
- **Orders & OrderDetails:** Handles transactions & fulfillment status.
- **Cart & CartItems:** Temporary storage before checkout.
- **Reviews:** Stores user ratings & comments.
- **Notifications:** Tracks order updates.

---

## Setup & Installation
1 **Clone the repository**
```bash
git clone https://github.com/MrBottleTree/Amazoff.git
cd amazoff
```

```

3 **Apply migrations**
```bash
python manage.py migrate
```

4 **Create a superuser (for admin access)**
```bash
python manage.py createsuperuser
```

5 **Run the development server**
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** to access the platform.

---

## Usage Guide
- **Sellers**: Add products, manage inventory, fulfill orders.
- **Buyers**: Browse products, add to cart, checkout, track orders.
- **Admins**: Manage users, categories, and overall platform settings.

---

## Future Improvements
Integrate **payment gateway** for wallet transactions.  
Add **filtering** for better product discovery.  
Improve **real-time notifications** using WebSockets.

---

## Contributors
- **Vishrut Ramraj** - Developer & Maintainer

---
**Amazoff - Not so prime!**
