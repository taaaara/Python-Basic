# Comparison Operators
# The results of the comparison operation is always True or False.
# ==    : True if the same, False if different
# !=    : True if different, False if same
# <     : True if the right side is larger (excluding equal values), otherwise return False
# >     : True if the left side is larger  (excluding equal values), otherwise return False
# <=    : True if the right side is larger or equal, otherwise return False
# >=    : True if the left side is larger or equal, otherwise return False

# print(5 != 2)
# print(5 < 2)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# if(condition):
#   Run if the above condition is True.
# elif(condition) :
#   Run elif the above condition is True.
# else :
#   Run if  all condition are False

# if    : always use 1
# elif  : use range  0 ~ infinity
# else  : use 0 or 1
# if can be used by nesting within if. 


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# 100 ~ 90  : A
# 89 ~ 70   : B
# 69 ~ 60   : C
# 59 ~      : D

# score = int(input())

# if(100 >= score >= 90):
#     print('A')
# elif(89 >= score >= 70):
#     print('B')
# elif(69 >= score >= 60):
#     print('C')
# elif(59 >= score >= 0):
#     print('D')

# print("End")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



# age = int(input("Enter your age: "))  # always with variable

# if(12 < age):
#     print("Good, have fun watching.")
# elif(12 > age):
#     print("Sorry, only over 12 years can watch the movie.")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


# print("Enter Number")
# number = int(input())       # int

# if(number % 2 == 0):        # use 0
#     print('Even')
# elif(number % 2 != 0):
#     print("Odd")



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# not   : If True, the results is reversed to False. If False, the result is reversed to True.
# and   : True if both sides are True, False if even one side is False
# or    : False if both sides are False, True if at least one side is True
# The execution order is executed in the order of not, and, and or.

# print(not(1==1))
# print(1 != 5) and (10 <= 15)
# print((6 != 6)) or (5 == 3)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# print('Enter 2 numbers')
# number = int(input())
# number2 = int(input())

# print('What calculation do you want to use?')
# print('(1: Multiply, 2: Divide, 3: Add, 4: Subtract)')
# calculation = int(input())
# if(calculation == 1):
#     print('Selected multiply,', number,'*',number2,'=',number*number2)
# elif(calculation == 2):
#     print('Selected division,', number,'/',number2,'=',number/number2)
# elif(calculation == 3):
#     print('Selected addition,', number,'+',number2,'=',number+number2)
# elif(calculation == 4):
#     print('Selected substraction,', number,'-',number2,'=',number-number2)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


# Nested if
# if can be nested

# age = int(input("Enter your age: "))
# # is_member = input('Are you a member? (yes or no):')

# if (age >= 18):
#     if(is_member == "yes"):
#         print('Welcome, adult member!')
#     else:
#         print("Adult non-member, please sign up.")
# else:
#     if(is_member == 'yes'):
#         print('Welcome, young member!')
#     else:
#         print('Young non-member, please sign up.')