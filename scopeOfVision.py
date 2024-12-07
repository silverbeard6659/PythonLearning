variable1 = 'im out of scope'
def my_function():
    variable1 = 'im inside a function'
    loval_var = "i'm local variable"
    print(loval_var)
    print(variable1)
    
my_function()
#print(local_var)
#print(variable1)