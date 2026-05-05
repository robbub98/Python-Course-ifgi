# this module is a calculator with the four basic calculation methods
# that use the variables a and b for calculating the result

class Calculator:

    # Constructor
    def __init__(self) -> None:
        pass

    # Addition
    def add(self, a, b):
        return a + b
    
    # Subtraction
    def sub(self, a, b):
        return a - b
    
    # Multiplication
    def multply(self,a,b):
        return a * b
    
    # Division
    # detects division by zero, which is not a possible calculation
    # and prints error message
    def divd(self,a,b):
        if b == 0:
            return "ZeroDivisionError : cannot divide by zero"
        else:
            return int(a/b)