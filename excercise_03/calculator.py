# this module is a calculator with the four basic calculation methods
# that use the variables a and b for calculating the result

# Addition
# Subtraction
# Multiplication
# Division

class Calculator:


    def __init__(self) -> None:
        pass
    
    def add(self, a, b):
        return a + b
    
    def sub(self, a, b):
        return a - b
    
    def multply(self,a,b):
        return a * b
    
    # detects division by zero, which is not a possible calculation
    # and prints error message
    def divd(self,a,b):
        if b == 0:
            return "ZeroDivisionError : cannot divide by zero"
        else:
            return int(a/b)