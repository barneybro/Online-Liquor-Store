# 🛒 Flask-Based Liquor Store Website

This Flask-based website is a comprehensive platform for users to interact with a liquor store, offering various functionalities depending on their role (**customer** or **vendor**).  

---

## 🔑 User Authentication

### **Login**
- Users log in using their email and password.
- The system validates credentials and redirects them to the appropriate dashboard (**customer** or **vendor**).  

### **Register**
- New users create an account by providing:
  - Email  
  - Password  
  - First name & last name  
  - Account type (**customer** or **vendor**)  
- Passwords are securely hashed before storage.  

---

## 🛍️ Product Browsing & Purchasing

### **Browse Products**
- View all available products, including:  
  - Name  
  - Price  
  - Description  
  - Image  
- Products are categorized (e.g., **vodka, whiskey, tequila**) for easy navigation.  

### **Add to Cart**
- Users can add products to their shopping cart and specify the quantity.  

### **View Cart**
- View items in the cart, update quantities, or remove items before checkout.  

### **Checkout**
- Complete purchases, creating an order in the database and clearing the cart.  

---

## 🏪 Product Management (Vendors)

### **Add Products**
- Vendors add new products by providing:  
  - Name  
  - Price  
  - Description  
  - Image  
  - Stock  
  - Category  

### **Edit Products**
- Vendors update product details (**name, price, description, image, stock**).  

### **Delete Products**
- Soft delete products (removes them from storefront but keeps them in the database).  

### **Add Discounts**
- Vendors apply discounts, specifying the amount and duration.  

---

## 📦 Order Management

### **Customer Orders**
- Customers view order history and track order status.  

### **Vendor Orders**
- Vendors can:  
  - View all orders for their products.  
  - Update order status (**pending, shipped, delivered**).  

---

## ⭐ Reviews & Feedback

### **Submit Reviews**
- Customers leave reviews for purchased products, including:  
  - A rating  
  - Written feedback  

### **View Reviews**
- All users can see customer reviews on product pages.  

---

## ⚙️ Account Management

### **User Profile**
- Customers can view and update their account details.  

### **Vendor Profile**
- Vendors can manage their account and listed products.  

---

## 🛠️ Admin & Vendor Actions

### **Update Order Status**
- Vendors can update order statuses (**pending → shipped → delivered**).  

### **Handle Claims**
- Vendors can manage customer claims/complaints and update their resolution status.  

---

## 🔐 Security & Validation

### **Password Hashing**
- User passwords are securely hashed using **SHA-1** before storage.  

### **Session Management**
- Flask sessions manage user authentication and store user-specific data (**user ID, email, account type**).  

---

This website provides a **seamless experience** for both customers and vendors:  
✅ **Customers** can browse, purchase, and review products.  
✅ **Vendors** can manage inventory, orders, and discounts effectively.  
