from operator import index
from random import randint


numbers = [52,32,56,753,634,64,75,3,2,6,234,7,32,4,32,634,22,1,3,123,1523,2367,33,43,23,23]
random_numbers=[]
even_numbers=[]
count=10
i=0
while i < count:
    random_numbers.append(randint(1,1000))
    i += 1
print(random_numbers)
for number in random_numbers:
    if number%2 == 0:
        even_numbers.append(number)
        continue
    print(number)
print(even_numbers)

for i in range(len(numbers)):
    numbers[i] += 1
print(numbers)
print("_________")

greeting = "hellooooooooooo, world! im just chechking sum of O's"
indexes = []
i = 0
for i in range(len(greeting)):
    if greeting[i] == 'o' or greeting[i] == 'O':
        i += 1
        indexes.append(i)
print(f"There is this much letters 'o' big or small -> {indexes}")

