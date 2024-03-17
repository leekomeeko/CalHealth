import tkinter as tk

def add_meal():
    meal_name = meal_entry.get()
    calorie_count = calorie_entry.get()

    if not meal_name or not calorie_count.isdigit():
        return

    with open('Datafile/meals.txt', 'a') as file:
        file.write(f'{meal_name}: {calorie_count}\n')
        

    meal_entry.delete(0, tk.END)
    calorie_entry.delete(0, tk.END)

root = tk.Tk()
root.title("CalHealth")

meal_label = tk.Label(root, text="Meal Name:")
meal_label.pack()

meal_entry = tk.Entry(root)
meal_entry.pack()

calorie_label = tk.Label(root, text="Calorie Count:")
calorie_label.pack()

calorie_entry = tk.Entry(root)
calorie_entry.pack()

add_button = tk.Button(root, text="Add Meal", command=add_meal)
add_button.pack()

root.mainloop()