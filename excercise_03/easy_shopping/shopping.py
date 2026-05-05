# this module contains a class named shoppingCart
# 

class ShoppingCart:

    # Constructor that initializes count count
    # and the list items
    def __init__(self):
       self.count = 0
       self.items = []

    # method to add an item and its quantity
    # to list items
    def addItem(self, itemName, qty):
        return self.items.append((itemName, qty))

    # method to remove item from list items
    def remvItem(self, item):
       for a in self.items:
            if (a[0] == item):
                return self.items.remove(a) 
    
    # method to print contents from list items
    # prints item name and its quantity and 
    # the total amount of items in list items
    def totalItems(self):
        self.count = 0
        print('The shopping cart contains: ')
        for a in self.items:
            print(a[0],'  -  ',a[1])
            self.count += a[1]
        return print('The total amount of items is: ', self.count,'\n')