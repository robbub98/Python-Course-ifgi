# Runs test for excercise 3 in Pyhton in QGIS &
# ArcGIS course at University of Münster


# import class Calculator from module calculator
from calculator import Calculator

# import class ShoppingCart from module shopping
from shopping import ShoppingCart

# method main that runs tests for excercises
def main() -> None:

    # create instance calc from class Calculator
    calc = Calculator()

    # run tests for task 3.1.1 each method from Calculator
    print('\n''Tests for task 3.1.1')
    print('7 + 5 = ', calc.add(7,5))
    print('34 - 21 = ', calc.sub(34,21))
    print('54 * 2 = ', calc.multply(54,2))
    print('144 / 2 = ', calc.divd(144,2))
    print('45 / 0 = ', calc.divd(45,0), '\n')

    # create instance shpCrt from class ShoppingCart
    shpCrt = ShoppingCart()

    # run tests for task 3.1.2 each method from ShoppingCart
    # by adding and removing items in shpCrt and prints
    # items names and quantity and totatl number of items
    print('\n''Tests for task 3.1.2''\n''Adding Items...')
    shpCrt.addItem('Bratwurst', 4)
    shpCrt.addItem('Feldsalat', 2)
    shpCrt.addItem('Kartoffel', 1)

    shpCrt.totalItems()
    print('Removing item...')
    shpCrt.remvItem('Feldsalat')
    shpCrt.totalItems()


    
if __name__ == "__main__":
    main()