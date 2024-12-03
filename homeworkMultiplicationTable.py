# print math multiplication table with using cycles:
# 1 * 1 = 1
# 2 * 2 = 4
# ...
# 9 * 9 = 81

# solution:
# input number of rows and columns
#row = input(f"input number of rows: ")
row = 9
i = 1
print(f"your multiplication table will be: {row} rows")
print(f"your multiplication table will be look like this:")
while i <= row:
    while i <= row:
        print(f"{i} * {i} = {i*i}")
        i += 1
