def count_vowels(string):
    VOWELS = "aeiouAEIOU"
    count = 0
    for char in string:
        if char in VOWELS:
            count += 1
            
    return count

print(count_vowels("Hello world"))
print(count_vowels("python is a very powerful language."))

def nothing():
    #print("this function does nothing")
    pass
    
nothing()

# the * symbol below was added for strong typing,
# and -> str thingy is for making return expected to by that -> type (функция вернёт значение, но это скорее метка для других сотрудников);
def format_date(*,day:int, month:str) -> str:
    return f"The date is {day} of {month}"

print(format_date(day=15,month="October"))
print(format_date(month="january",day=1))