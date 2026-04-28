# exercise_2_1.py
# Author: robbub98
# Date: 2026-04-28
# Description: Exercise 2.1 — Three basic Python functions
# for the Python in QGIS & ArcGIS course.

# donuts
# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    if isinstance(count, int)==True:
        if count >= 10:
            return "Count: Many"
        else: 
            return "Count: " + str(count)
    else: 
        return "Your input is not an integer!"

# verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    if s.len()>= 3:
        if s.
        s.append('ing')
    
    
    return  

def remove_adjacent(nums):
# +++ your code here +++
    return

def main():
    print('donuts')
    print(donuts(4))
    print(donuts(9))
    print(donuts(10))
    print(donuts('twentyone'))
    print('verbing')
    print(verbing('hail'))
    print(verbing('swiming'))
    print(verbing('do'))
    print('remove_adjacent')
    print(remove_adjacent([1, 2, 2, 3]))
    print(remove_adjacent([2, 2, 3, 3, 3]))
    print(remove_adjacent([]))


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()