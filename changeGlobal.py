#set global variable
global_var = "i'm global variable"

def globalization():
    global global_var
    global_var =  "i am changed global variable"

print(global_var)
globalization()
print(global_var)



#check mmorpg leveling up needs
DEFAULT_LEVEL_EXPERIENCE1 = 200


def is_leveled_up(*, current_exp:int, gained_exp:int) -> bool:
    total_exp = current_exp + gained_exp
    level_up = False
    if total_exp >= DEFAULT_LEVEL_EXPERIENCE1:
        level_up = True
    
    return level_up


print(is_leveled_up(current_exp=150, gained_exp=60))
print(is_leveled_up(current_exp=10,gained_exp=60))