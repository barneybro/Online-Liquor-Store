This Flask-based website is a comprehensive platform for users to interact with a liquor store, offering a variety of functionalities depending on their role (customer or vendor). Here are some of the key actions users can perform on this website:

User Authentication:

Login: Users can log in using their email and password. The system validates their credentials and redirects them to the appropriate dashboard based on their account type (customer or vendor).

Register: New users can create an account by providing their email, password, first name, last name, and account type (customer or vendor). Passwords are securely hashed before being stored in the database.

Product Browsing and Purchasing:

Browse Products: Users can view all available products, including details like name, price, description, and image. Products are categorized (e.g., vodka, whiskey, tequila) for easy navigation.

Add to Cart: Users can add products to their shopping cart and specify the quantity they wish to purchase.

View Cart: Users can see the items in their cart, update quantities, or remove items before proceeding to checkout.

Checkout: Users can complete their purchase, which creates an order in the database and clears their cart.

Product Management (Vendors):

Add Products: Vendors can add new products to the store by providing details like name, price, description, image, stock, and category.

Edit Products: Vendors can update product details, such as name, price, description, image, and stock.

Delete Products: Vendors can "soft delete" products by marking them as deleted, which removes them from the storefront but keeps them in the database.

Add Discounts: Vendors can apply discounts to products, specifying the discount amount and duration.

Order Management:

Customer Orders: Customers can view their order history and track the status of their orders.

Vendor Orders: Vendors can view all orders placed for their products and update the order status (e.g., pending, shipped, delivered).

Reviews and Feedback:

Submit Reviews: Customers can leave reviews for products they’ve purchased, including a rating and written feedback.

View Reviews: All users can see reviews left by other customers on product pages.

Account Management:

User Profile: Customers can view and manage their account information.

Vendor Profile: Vendors can view their account information and manage their listed products.

Admin and Vendor Actions:

Update Order Status: Vendors can update the status of orders (e.g., from "pending" to "shipped").

Handle Claims: Vendors can manage customer claims or complaints, updating their status as resolved or pending.

Security and Validation:

Password Hashing: User passwords are securely hashed using SHA-1 before being stored in the database.

Session Management: The website uses Flask sessions to manage user authentication and store user-specific data (e.g., user ID, email, account type).

This website provides a seamless experience for both customers and vendors, enabling customers to browse, purchase, and review products, while vendors can manage their inventory, orders, and discounts effectively.
