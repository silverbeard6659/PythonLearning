user_roles = ("admin", "editor", "viewer")
for role in user_roles:
    print(role)
    
print("admin" in user_roles)

print(user_roles[1], user_roles[2])

not_tuple = ("admin")
print(type(not_tuple))

definetely_tuple = ("admin",)
print(type(definetely_tuple))