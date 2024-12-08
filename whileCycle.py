from pydantic import MySQLDsn


counter = 1

while counter <= 5:
    print(f"counter is: {counter}")
    counter += 1
    
my_list = [0,1,2,3,4,5]

while my_list:
    print(f"my_list have: {my_list}")
    my_list.pop()
    
print(f"my_list have: {my_list}")

while True:
    answer = input(f"insert a number: ")
    if answer == "quit":
        print("you have quitted")
        break
    print(f"you've entered: {answer}")