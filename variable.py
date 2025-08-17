# variable = value
# Save the value in variable in the format above
# = Unlike the meaning of the symbol, the value is simply stored in a variable.
# Variable can be whatever you want as long as you follow the rules below.
# 1. Impossible to start with a number
# 2. Special characters are not possible except the symbol "_"
# 3. No spacing
# 4. Reserved words not possible

# my_name = "Tara"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# Data  types 
# str   -> String       => made up of quotes " " ''
# float -> Float        => no quotes and has a deciaml point
# int   -> Integer      => no quotes and no decimal point
# Everyday words (English, Chinese, Korean, etc.) without quotes => error

# a = 10      # saves the integer 10 in the variable a
# b = 'cit'   # saves the string 'cit' in the variable b

# name = 'Tara'
# age = 10
# height = 148


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# print ('text' or variable or number)
# The print () function prints the 'text', number, or value of
# the variable inside the bracket and then adds a newline.
# To print multiple items, use a comma (,)
# If you use print() with nothing inside, it prints an empty line

# name = 'Tara'
# age = 10
# height = 148
# print(name)
# print()     #prints an empty line
# print(age)
# print(height)
# print('hi')
# print()
# print(5)
# print(5*10)
# print(name, age, height, "hello")


# # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# # Problem
# Create two variable(name, school).
# Make it so that the following content is displaying when run

# name = 'Tara'
# school = 'YISS'
# print('Hello, my name is', name)
# print('I am currently a 5th grade student at' ,school)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


# Type casting
# str(variable or value)    => converts variable or value to str data type
# float(variable or value)  => converts variable or value to float data type
# int(variable or value)    => converts variable or value to int data type
# Just using them in calculation doesn't change the original variable's data type
# To change the original variable's data type, save it back into the variable [ex. a=int(a)]

# var1 = 2
# var2 = '31'
# result = var1 + int(var2)   # saves var1 + var2 converted to int in result
# print(result)
# print(type(var2))           # prints the data type of var2, which is still str
# var2 = int(var2)            # converts var2 to int and saves it back in var2
# print(type(var2))           # prints the new data type of var2


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#



# input('text' or value or variable)
# Displays 'text' or the value of the variable, then waits for keyboard input until Enter is pressed 
# 'text' or variable can be left out
# variable = input('text' or variable)
# usually used in this format, without variable it hte input is not saved 
# input () always saves the valur as a str data type

# var = 2
# var2 = input("Insert anything")
# print(var2)
# print(type(var2))

# var2 = int(var2)
# print(type(var2))

# sum= var1 + var2
# print(sum)



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #



# +     add
# -     subtract
# *     multiply
# /     divide (result is a float)
# //    integer division (result is an int)
# %     modulus (remainder)
# **    exponet (power)

# a = 10
# b= 3
# print(a+b)
# print(a-b)
# print(a*b)
# print(a/b)
# print(a//b)
# print(a%b)
# print(a**b)