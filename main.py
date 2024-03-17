import tkinter as tk
from tkinter import ttk
import TKinterModernThemes as TKMT
import csv
import datetime
import os
import pandas as pd

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Final Project", theme, mode, usecommandlineargs, usethemeconfigfile)
        self.master.title("Program Beta")
        self.master.geometry("800x600")
        self.master.config(bg='#FEFFF2')
        self.master.resizable(False, False)
        self.startmenu()
        self.run()
        self.username = ""

    
    title_font = ("Segoe UI Black", 36)
    heading_font = ("Segoe UI Semibold", 24)
    text_font = ("Segoe UI", 12)
    color_bg = '#FEFFF2'
    def startmenu(self):
        def check_entry():
            if self.username_entry.get() == "":
                self.button.config(state="disabled")
            else:
                self.username = self.username_entry.get()
                self.button.config(state="normal")

        def username_get():
            self.username = self.username_entry.get()
            self.mainmenu()

        title = tk.Label(self.master, text="CalHealth", font=self.title_font, bg= self.color_bg)
        title.place(relx=0.5, rely=0.35, anchor="center")
        description = tk.Label(
            self.master,
            text="The CalHealth is an application designed to promote healthy living by \nproviding health-conscious people an easy way to calculate he amount of \ncalories eaten per meal and plan succeeding meals based on the results.",
            font=self.text_font, bg= self.color_bg
        )
        description.place(relx=0.5, rely=0.6, anchor="center")

        Username = tk.Label(self.master, text="Username:", font=self.text_font, bg= self.color_bg)
        Username.place(relx=0.32, rely=0.78, anchor="center")
        self.username_entry = tk.Entry(font=self.text_font, width=30, borderwidth=2, relief="groove")
        self.username_entry.place(relx=0.55, rely=.78, anchor="center")

        self.button = tk.Button(self.master, text="Start Program", command=username_get, state='disabled')
        self.button.place(relx=0.5, rely=0.9, anchor="center")
        self.username_entry.bind("<KeyRelease>", lambda _: check_entry())



    def mainmenu(self):
        def save_username(): 
            with open('Datafile/USERS/User_list.txt', 'r') as file:
                existing_user_list = [line.strip() for line in file]
            if self.username not in existing_user_list:
                with open('Datafile/USERS/User_list.txt', 'a') as file:
                    file.write('\n'+self.username)

        for widget in self.master.winfo_children():
            widget.destroy()
        print("Main Menu launched!")
        with open('Datafile/USERS/User_list.txt', 'r') as file:
            existing_user_list = [line.strip() for line in file]
        def exit_program():
            self.master.destroy()
        def delete_user():
            # Delete user folder
            user_folder = f"Datafile/USERS/{self.username}"
            if os.path.exists(user_folder):
                for file_name in os.listdir(user_folder):
                    file_path = os.path.join(user_folder, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)

                os.rmdir(user_folder)
            
            # Remove username from user_list.txt
            with open('Datafile/USERS/User_list.txt', 'r') as file:
                lines = file.readlines()
            with open('Datafile/USERS/User_list.txt', 'w') as file:
                for line in lines:
                    if line.strip() != self.username:
                        file.write(line)

            for widget in self.master.winfo_children():
                widget.destroy()
            self.startmenu()


        if self.username in existing_user_list:
            welcome = tk.Label(self.master, text=f"Welcome back {self.username}", font=self.heading_font, bg= self.color_bg)
            welcome.place(relx=0.06, rely=0.08)

            def display_bmr_data():
                username_bmr_file = f"Datafile/USERS/{self.username}/{self.username}_BMR.csv"
                try:
                    bmr_data = pd.read_csv(username_bmr_file)
                    latest_results = bmr_data.tail(10)

                    # Create a ttk Treeview widget
                    table = ttk.Treeview(self.master, columns=list(latest_results.columns), show="headings")
                    
                    # Add columns to the table
                    for column in latest_results.columns:
                        table.heading(column, text=column)
                    
                    # Add data to the table
                    for row in latest_results.itertuples(index=False):
                        table.insert("", "end", values=row)
                    
                    table.place(relx=0.65, rely=0.4, anchor='center')  # Modify the position of the table
                except FileNotFoundError:
                    print(f"File {username_bmr_file} not found.")

            display_bmr_data()
        else:
            welcome = tk.Label(self.master, text=f"Welcome to CalHealth {self.username}", font=self.heading_font, bg= self.color_bg)
            save_username()
            welcome.place(relx=0.06, rely=0.08)

        option_1 = tk.Button(self.master, text="Calculate Daily \nCaloric Intake", padx=24, pady=6, width=15, command=self.Calculate_Calories)
        option_1.place(relx=0.2, rely=0.3, anchor="center")

        option_2 = tk.Button(self.master, text="Plan Meals", padx=24, pady=6, width=15, command=self.Plan_Meals)
        option_2.place(relx=0.2, rely=0.5, anchor="center")

        option_3 = tk.Button(self.master, text="Caloric History", padx=24, pady=6, width=15, command=self.Caloric_History)
        option_3.place(relx=0.2, rely=0.7, anchor="center")

        return_button = tk.Button(self.master, text="Exit Program", command=exit_program)
        return_button.place(relx=0.88, rely=0.9, anchor="center")

        delete_button = tk.Button(self.master, text="Delete User", command=delete_user)
        delete_button.place(relx=0.75, rely=0.9, anchor="center")

    def Calculate_Calories(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        print("Calculate Calories launched!")

        def val_check():
            age = self.age_entry.get()
            gender = self.gender_var.get()
            height = self.height_entry.get()
            weight = self.weight_entry.get()

            if not age.isdigit():
                self.invalid_label.config(text="Invalid value", fg="red")
                self.age_entry.config(bg="red")
            else:
                self.age_entry.config(bg="white")

            if not height.isdigit():
                self.invalid_label.config(text="Invalid value", fg="red")
                self.height_entry.config(bg="red")
            else:

                self.height_entry.config(bg="white")

            if not weight.isdigit():
                self.invalid_label.config(text="Invalid value", fg="red")
                self.weight_entry.config(bg="red")
            else:
                self.weight_entry.config(bg="white")
                
            if not gender:
                self.invalid_label.config(text="Please indicate gender", fg="red")
            else:
                self.invalid_label.config(text="")

            if age.isdigit() and height.isdigit() and weight.isdigit() and gender:
                calculate_bmr()


        def calculate_bmr():
            age = int(self.age_entry.get())
            weight = int(self.weight_entry.get())
            height = int(self.height_entry.get())
            if self.gender_var.get() == "M":
                bmr = (88.4 + 13.4 * weight) + (4.8 * height) - (5.68 * age)
            elif self.gender_var.get() == "F":
                bmr = (447.6 + 9.25 * weight) + (3.10 * height) - (4.33 * age)
                self.bmr_value = tk.Label(self.master, text=f"{round(bmr)}", font=self.text_font, bg=self.color_bg)
                self.bmr_value.place(relx=0.775, rely=0.2, anchor="w")
            if bmr:
                proceed_button.config(state="normal")
                bmr_label = tk.Label(self.master, text="BMR:", font=self.text_font, bg=self.color_bg)
                bmr_label.place(relx=0.775, rely=0.2, anchor="e")
                maintain_weight_label = tk.Label(self.master, text="Maintain Weight:", font=self.text_font, bg=self.color_bg)
                maintain_weight_label.place(relx=0.775, rely=0.3, anchor="e")
                maintain_weight_calories = round(bmr)
                maintain_weight_value = tk.Label(self.master, text=f"{maintain_weight_calories} calories/day", font=self.text_font, bg=self.color_bg)
                maintain_weight_value.place(relx=0.775, rely=0.3, anchor="w")

                mild_weight_loss_label = tk.Label(self.master, text="Mild Weight Loss:", font=self.text_font, bg=self.color_bg)
                mild_weight_loss_label.place(relx=0.775, rely=0.4, anchor="e")
                mild_weight_loss_calories = round(bmr * 0.91)
                mild_weight_loss_value = tk.Label(self.master, text=f"{mild_weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                mild_weight_loss_value.place(relx=0.775, rely=0.4, anchor="w")

                weight_loss_label = tk.Label(self.master, text="Weight Loss:", font=self.text_font, bg=self.color_bg)
                weight_loss_label.place(relx=0.775, rely=0.5, anchor="e")
                weight_loss_calories = round(bmr * 0.82)
                weight_loss_value = tk.Label(self.master, text=f"{weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                weight_loss_value.place(relx=0.775, rely=0.5, anchor="w")

                extreme_weight_loss_label = tk.Label(self.master, text="Extreme Weight Loss:", font=self.text_font, bg=self.color_bg)
                extreme_weight_loss_label.place(relx=0.775, rely=0.6, anchor="e")
                extreme_weight_loss_calories = round(bmr * 0.64)
                extreme_weight_loss_value = tk.Label(self.master, text=f"{extreme_weight_loss_calories} calories/day", font=self.text_font, bg=self.color_bg)
                extreme_weight_loss_value.place(relx=0.775, rely=0.6, anchor="w")

                username = self.username
                folder_path = f"Datafile/USERS/{username}"
                os.makedirs(folder_path, exist_ok=True)

                filename = f"{folder_path}/{username}_BMR.csv"
                with open(filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    if file.tell() == 0:
                        writer.writerow(["Name", "Data"])
                    writer.writerow(["Date", datetime.date.today()])
                    writer.writerow(["User", username])
                    writer.writerow(["Age", age])
                    writer.writerow(["Weight", weight])
                    writer.writerow(["Height", height])
                    writer.writerow(["Gender", self.gender_var.get()])
                    writer.writerow(["BMR", round(bmr)])
                    writer.writerow(["Maintain Weight", maintain_weight_calories])
                    writer.writerow(["Mild Weight Loss", mild_weight_loss_calories])
                    writer.writerow(["Weight Loss", weight_loss_calories])
                    writer.writerow(["Extreme Weight Loss", extreme_weight_loss_calories])
                    writer.writerow([])  # Add an empty row after the last data

        welcome = tk.Label(self.master, text=f"Calorie Calculator", font=self.text_font, bg=self.color_bg)
        welcome.place(relx=0.5, rely=0.08, anchor="center")
        
        age_label = tk.Label(self.master, text="Age:", font=self.text_font, bg=self.color_bg)
        age_label.place(relx=0.12, rely=0.2, anchor="center")
        self.age_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.age_entry.place(relx=0.3, rely=0.2, anchor="center")

        gender_label = tk.Label(self.master, text="Gender:", font=self.text_font, bg=self.color_bg)
        gender_label.place(relx=0.12, rely=0.3, anchor="center")
        self.gender_var = tk.StringVar()
        self.male_checkbox = tk.Radiobutton(self.master, variable=self.gender_var, value="M", font=self.text_font, bg=self.color_bg)
        self.male_checkbox.place(relx=0.2, rely=0.3, anchor="center")
        self.male_label = tk.Label(self.master, text="Male", font=self.text_font, bg=self.color_bg).place(relx=0.25, rely=0.3, anchor="center")

        self.female_checkbox = tk.Radiobutton(self.master, variable=self.gender_var, value="F", font=self.text_font, bg=self.color_bg)
        self.female_checkbox.place(relx=0.32, rely=0.3, anchor="center")
        self.female_label = tk.Label(self.master, text="Female", font=self.text_font, bg=self.color_bg).place(relx=0.37, rely=0.3, anchor="center")
        self.gender_var.set(None)

        height_label = tk.Label(self.master, text="Height (cm):", font=self.text_font, bg=self.color_bg)
        height_label.place(relx=0.12, rely=0.4, anchor="center")
        self.height_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.height_entry.place(relx=0.3, rely=0.4, anchor="center")

        weight_label = tk.Label(self.master, text="Weight (kg):", font=self.text_font, bg=self.color_bg)
        weight_label.place(relx=0.12, rely=0.5, anchor="center")
        self.weight_entry = tk.Entry(font=self.text_font, width=20, borderwidth=2, relief="groove")
        self.weight_entry.place(relx=0.3, rely=0.5, anchor="center")

        calculate_button = tk.Button(self.master, text="Calculate BMR", command=val_check)
        calculate_button.place(relx=0.3, rely=0.6, anchor="center")

        
        self.invalid_label = tk.Label(self.master, text="", font=self.text_font, bg=self.color_bg)
        self.invalid_label.place(relx=0.3, rely=0.7, anchor="center")




        
        proceed_button = tk.Button(self.master, text="Proceed to Meal Plan", command=self.Plan_Meals, state="disabled")
        proceed_button.place(relx=0.7, rely=0.9, anchor="center")
        
        return_button = tk.Button(self.master, text="Return to Main Menu", command=self.mainmenu)
        return_button.place(relx=0.9, rely=0.9, anchor="center")

 

    def Plan_Meals(self):
        self.total_calories = 0
        for widget in self.master.winfo_children():
            widget.destroy()
        print("Plan Meals launched!")
        def import_dictionary(filename):
            dictionary = {}
            with open(filename, 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')
                    dictionary[key.strip()] = value.strip()
            return dictionary

        imported_dict = import_dictionary('Datafile/meals.txt')


        listbox = tk.Listbox(self.master, width=36, height=10, font=self.text_font, bg= "white", borderwidth=2, relief="groove")
        listbox.place(relx=0.25, rely=0.35, anchor="center")

        for key in imported_dict.keys():
            listbox.insert(tk.END, f"{key}")


        value_label = tk.Label(self.master, text="Calories per serving: ", font=self.text_font, bg=self.color_bg)
        value_label.place(relx=0.05, rely=0.78, anchor="w")

        def display_value(event):
            selected_key = listbox.get(listbox.curselection())
            selected_value = imported_dict[selected_key]
            value_label.config(text=f"Calories Per serving: {selected_value} Calories")

        listbox.bind('<<ListboxSelect>>', display_value)
        
        def add_meal():
            meal_name = meal_entry.get()
            calorie_count = calorie_entry.get()

            if not meal_name or not calorie_count.isdigit():
                return

            imported_dict[meal_name] = calorie_count

            with open('Datafile/meals.txt', 'a') as file:
                file.write(f'{meal_name}: {calorie_count}\n')

            meal_entry.delete(0, tk.END)
            calorie_entry.delete(0, tk.END)
            listbox.insert(tk.END, f"{meal_name}")
        
        def add_mealbox():
            meal_name = meal_pick.get()
            if meal_name in imported_dict:
                calorie_count = imported_dict[meal_name]
                mealbox.insert(tk.END, f"{meal_name} - {calorie_count} Calories")
                self.total_calories += int(calorie_count)
                total_calories_label.config(text=f"Total Calories: {self.total_calories}")



        def delete_from_mealbox():
            selected_index = mealbox.curselection()
            if selected_index:
                selected_item = mealbox.get(selected_index)
                meal_name = selected_item.split(" - ")[0]
                calorie_count = selected_item.split(" - ")[1].split(" ")[0]
                mealbox.delete(selected_index)
                self.total_calories -= int(calorie_count)
                total_calories_label.config(text=f"Total Calories: {self.total_calories}")
        
        def save_meal_history():
            # Create the directory if it doesn't exist
            directory = f"Datafile/USERS/{self.username}"
            os.makedirs(directory, exist_ok=True)

            file_path = f"{directory}/{self.username}_meals.csv"

            current_datetime = datetime.date.today()

            selected_meals = []
            for i in range(mealbox.size()):
                meal = mealbox.get(i)
                meal_name = meal.split(" - ")[0]
                calorie_count = meal.split(" - ")[1].split(" ")[0]
                selected_meals.append((meal_name, calorie_count))

            # Calculate the total calories
            total_calories = sum(int(calorie) for _, calorie in selected_meals)

            # Write the data to the CSV file
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_datetime, selected_meals, total_calories])

            # Enable the proceed button
            proceed_button.config(state="normal")

        custom_meal_label = tk.Label(self.master, text="Custom Meal:", font=self.text_font, bg= self.color_bg)
        custom_meal_label.place(relx=0.25, rely=0.57, anchor="center")

        meal_label = tk.Label(self.master, text="Meal Name:", font=self.text_font, bg= self.color_bg)
        meal_label.place(relx=0.05, rely=0.62, anchor="w")

        meal_entry = tk.Entry(self.master)
        meal_entry.place(relx=0.2, rely=0.62, anchor="w")

        calorie_label = tk.Label(self.master, text="Calorie Count:", font=self.text_font, bg= self.color_bg)
        calorie_label.place(relx=0.05, rely=0.67, anchor="w")

        calorie_entry = tk.Entry(self.master)
        calorie_entry.place(relx=0.2, rely=0.67, anchor="w")

        add_button = tk.Button(self.master, text="Add \nMeal", command=add_meal)
        add_button.place(relx=0.42, rely=0.64, anchor="center")
    

        meal_button = tk.Button(self.master, text="Add to Meal", width=15, height=1, borderwidth=2, command=add_mealbox)
        meal_button.place(relx=0.31, rely=0.12, anchor="w")

        meal_pick = tk.Entry(self.master, width=29, borderwidth=2, relief="groove")
        meal_pick.place(relx=0.045, rely=0.12, anchor="w")

        def filter_listbox(_):
            try:
                filter_text = meal_pick.get().lower()
                listbox.delete(0, tk.END)
                for key in imported_dict.keys():
                    if filter_text in key.lower():
                        listbox.insert(tk.END, f"{key}")
            except Exception:
                pass

        meal_pick.bind("<KeyRelease>", filter_listbox)

        def select_from_listbox(_):
            try:
                selected_item = listbox.get(listbox.curselection())
                meal_pick.delete(0, tk.END)
                meal_pick.insert(tk.END, selected_item)
            except Exception:
                pass

        

        listbox.bind("<<ListboxSelect>>", select_from_listbox)

        mealbox = tk.Listbox(self.master, width=36, height=10, font=self.text_font, bg="white", borderwidth=2, relief="groove")
        mealbox.place(relx=0.75, rely=0.35, anchor="center")

        total_calories_label = tk.Label(self.master, text=f"Total Calories: {self.total_calories}", font=self.text_font, bg=self.color_bg)
        total_calories_label.place(relx=0.75, rely=0.78, anchor="center")

        delete_button = tk.Button(self.master, text="Delete", command=delete_from_mealbox, width=15, height=1, borderwidth=2)
        delete_button.place(relx=0.65, rely=0.12, anchor="center")

        save_button = tk.Button(self.master, text="Save Meal Plan", command=save_meal_history, width=15, height=1, borderwidth=2)
        save_button.place(relx=0.85, rely=0.12, anchor="center")



        proceed_button = tk.Button(self.master, text="Proceed to results", command=self.Caloric_History)
        proceed_button.place(relx=0.7, rely=0.9, anchor="center")
        
        return_button = tk.Button(self.master, text="Return to Main Menu", command=self.mainmenu)
        return_button.place(relx=0.9, rely=0.9, anchor="center")

    def Caloric_History(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        print("Caloric History launched!")

if __name__ == "__main__":
    App("sun-valley", "light")