# exercise_2_1.py
# Author: robbub98
# Date: 2026-04-28
# Description: Exercise 2.1 — Three basic Python functions
# for the Python in QGIS & ArcGIS course.

# Excercise 1 donuts
# Given an integer count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'


def donuts(count):
    # 1st if clause checks whether input is an integer
    # and if not tells user that input is not an integer
    if isinstance(count, int)==True:
        # 2nd if clause determines whether input integer
        # is greater equal 10 and acts then according the task 
        if count >= 10:
            return "Count: Many"
        else: 
            return "Count: " + str(count)
    else: 
        return "Your input is not an integer!"

# Excercise 2 Verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.

def verbing(s):
    # 1st if clause checks length of string s, if string
    # has lesser chars than 3 it returns the string
    if len(s)>= 3:
        # 2nd if clause checks whether string ends on 'ing'
        # if true it adds 'ly', if false it adds 'ing'
        if s[-3:] == "ing":
            s = s + "ly"
        else:
            s = s + "ing"
    return s
      
# Excercise 3 Remove adjacent
# Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.

def remove_adjacent(nums):
    # create new list result
    result = []
    # iterate over each entry of list nums
    for num in nums:
        # if result list ist empty or current entry does
        # not correspond to the last item on result, it
        # it adds current entry to result
        if len(result) == 0 or num != result[-1]:
            result.append(num)  
    return result

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