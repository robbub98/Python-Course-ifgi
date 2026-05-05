# Runs test for excercise 3 in Pyhton in QGIS &
# ArcGIS course at University of Münster


# import class Calculator from module calculator
from calculator import Calculator

# import class ShoppingCart from module shopping
from shopping import ShoppingCart

def main() -> None:
    # create instance calc from class Calculator
    calc = Calculator()

    # run tests for task 3.1.1 each method from Calculator
    print(calc.add(7,5))
    print(calc.sub(34,21))
    print(calc.multply(54,2))
    print(calc.divd(144,2))
    print(calc.divd(45,0))


    shpCrt = ShoppingCart()

    # run tests for task 3.1.2 each method from ShoppingCart
    # 
    shpCrt.addItem('Bratwurst', 4)
    shpCrt.addItem('Feldsalat', 2)
    shpCrt.addItem('Kartoffel', 1)
    
    shpCrt.totalItems()

    shpCrt.remvItem('Feldsalat')
    shpCrt.totalItems()


    
if __name__ == "__main__":
    main()