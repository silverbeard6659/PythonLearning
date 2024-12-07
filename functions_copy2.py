def custom_greeting(*, name: str = "vova",greeting: str = "hello") -> str:
    return f"{greeting}, {name}"

print(custom_greeting(name="pjetr",greeting="zdarova"))
print(custom_greeting())
print(custom_greeting(name="vasyan",greeting="good morning"))
print(custom_greeting(name="pjetr"))
print(custom_greeting(greeting="zdarova"))

input('Press ENTER to exit')