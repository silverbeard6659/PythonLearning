import random
import tkinter as tk
from tkinter import messagebox

def binary_search(lst, item):
    low = 0
    high = len(lst) - 1
    
    while low <= high:
        mid = (low + high) // 2  # Use integer division
        guess = lst[mid]
        if guess == item:
            return mid
        elif guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None

# Generate a sorted list of random numbers
def generate_random_sorted_list(size, start=1, end=100):
    try:
        if size > (end - start + 1):
            raise ValueError("Size is greater than the range.")
        random_list = random.sample(range(start, end + 1), size)
        random_list.sort()
        return random_list
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid range or size: {e}")
        return []

def search_item():
    try:
        size = int(size_entry.get())
        start = int(start_entry.get())
        end = int(end_entry.get())
        item = int(item_entry.get())
        
        random_list = generate_random_sorted_list(size, start, end)
        if not random_list:
            return
        
        index = binary_search(random_list, item)
        if index is not None:
            messagebox.showinfo("Result", f"Item {item} found at index {index}.\nGenerated list: {random_list}")
        else:
            messagebox.showinfo("Result", f"Item {item} not found in the list.\nGenerated list: {random_list}")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Create the main window
root = tk.Tk()
root.title("Binary Search with Random List")

# Create and place labels and entry fields
tk.Label(root, text="Size of the random list:").grid(row=0, column=0, padx=10, pady=5)
size_entry = tk.Entry(root)
size_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Start of the range:").grid(row=1, column=0, padx=10, pady=5)
start_entry = tk.Entry(root)
start_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="End of the range:").grid(row=2, column=0, padx=10, pady=5)
end_entry = tk.Entry(root)
end_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Item to search for:").grid(row=3, column=0, padx=10, pady=5)
item_entry = tk.Entry(root)
item_entry.grid(row=3, column=1, padx=10, pady=5)

# Create and place the search button
search_button = tk.Button(root, text="Search", command=search_item)
search_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
