#average
from random import randint

random_numbers=[]
count=10
i=0
while i < count:
    random_numbers.append(randint(1,1000))
    i += 1
print(f"your list of random numbers: {random_numbers}")
avg = sum(random_numbers) / len(random_numbers)
print(f"average is: {avg}")

def find_average_rand():
    random_numbers=[]
    count=10
    i=0
    while i < count:
        random_numbers.append(randint(1,1000))
        i += 1
    print(f"your list of random numbers: {random_numbers}")
    avg = sum(random_numbers) / len(random_numbers)
    print(f"average is: {avg}")
    return avg

print(find_average_rand())