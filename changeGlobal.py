#set global variable
global_var = "i'm global variable"

def globalization():
    global global_var
    global_var =  "i am changed global variable"

print(global_var)
globalization()
print(global_var)



#check mmorpg leveling up needs
DEFAULT_LEVEL_EXPERIENCE1