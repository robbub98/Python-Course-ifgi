# this module contains a class named shoppingCart

class ShoppingCart:

    def __init__(self):
       self.count = 0
       self.items = []

    def addItem(self, itemName, qty):
        return self.items.append((itemName, qty))

    def remvItem(self, item):
       for a in self.items:
            if (a[0] == item):
                return self.items.remove(a) 
    
    def totalItems(self):
        self.count = 0
        print('The shopping cart contains: ')
        for a in self.items:
            print(a[0],'  -  ',a[1])
            self.count += a[1]
        return print('The total amount of items is: ', self.count,'\n')