import easy_shopping
# Access the ShoppingCart class through the package
cart = easy_shopping.shopping.ShoppingCart()
cart.addItem("Test item", 5)
print(cart.totalItems())