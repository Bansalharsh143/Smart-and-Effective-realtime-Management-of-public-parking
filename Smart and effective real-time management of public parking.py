#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from datetime import datetime

def toggle_parking(event):
    widget = event.widget
    current_color = widget.cget("bg")
    new_color = "red" if current_color == "white" else "white"
    widget.config(bg=new_color)

def add_car():
    car_number = car_number_entry.get().strip()
    if car_number == "":
        return  # Prevent adding empty car numbers

    # Check if the car is already parked
    for car in car_data:
        if car['car_number'] == car_number:
            error_label.config(text=f"Car with number {car_number} is already parked!")
            error_label.after(3000, clear_error_message)
            return

    # Get current time
    in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Find the first empty parking spot
    for i, row in enumerate(parking_grid):
        for j, occupied in enumerate(row):
            if not occupied:
                parking_grid[i][j] = True  # Mark the parking spot as occupied

                # Store car data
                car_data.append({"car_number": car_number, "in_time": in_time, "parking_spot": f"{i+1}-{j+1}"})

                # Update car list display
                update_car_list()

                # Highlight the parking spot
                parking_spaces[i][j].config(bg="red")

                return

    # If no empty parking spot is found
    print("Parking is full!")

def remove_car():
    car_number = remove_car_entry.get()
    found = False
    for car in car_data:
        if car['car_number'] == car_number:
            # Assess out time
            out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            car['out_time'] = out_time

            # Mark the parking spot as empty in the parking grid
            row, col = map(int, car['parking_spot'].split("-"))
            parking_grid[row - 1][col - 1] = False
            parking_spaces[row - 1][col - 1].config(bg="white")

            # Update car list display
            update_car_list()
            found = True
            break

    if not found:
        error_label.config(text="Car not found in the list!")
        error_label.after(3000, clear_error_message)

def update_car_list():
    car_list_box.delete("1.0", tk.END)  # Clear the car list display
    for car in car_data:
        car_entry = f"Car: {car['car_number']} | Parking Spot: {car['parking_spot']} | In Time: {car['in_time']}"
        if 'out_time' in car:
            car_entry += f" | Out Time: {car['out_time']}"
        car_list_box.insert(tk.END, car_entry + "\n")

def clear_error_message():
    error_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Parking Management System")

    # Car data storage
    car_data = []

    # Car List Frame
    car_list_frame = tk.Frame(root)
    car_list_frame.grid(row=0, column=0, padx=10, pady=10)

    # Add Car UI
    car_number_label = tk.Label(car_list_frame, text="Car Number:")
    car_number_label.grid(row=0, column=0)
    car_number_entry = tk.Entry(car_list_frame)
    car_number_entry.grid(row=0, column=1)
    add_car_button = tk.Button(car_list_frame, text="Add Car", command=add_car)
    add_car_button.grid(row=0, column=2)

    # Remove Car UI
    remove_car_label = tk.Label(car_list_frame, text="Remove Car Number:")
    remove_car_label.grid(row=1, column=0)
    remove_car_entry = tk.Entry(car_list_frame)
    remove_car_entry.grid(row=1, column=1)
    remove_car_button = tk.Button(car_list_frame, text="Remove Car", command=remove_car)
    remove_car_button.grid(row=1, column=2)

    # Error Label
    error_label = tk.Label(car_list_frame, text="", fg="red")
    error_label.grid(row=2, column=0, columnspan=3)

    # Car List Display
    car_list_label = tk.Label(car_list_frame, text="Car List:")
    car_list_label.grid(row=3, column=0, columnspan=3)
    car_list_box = tk.Text(car_list_frame, width=100, height=10)  # Increased width
    car_list_box.grid(row=4, column=0, columnspan=3)

    # Spacer
    spacer_frame = tk.Frame(root, height=20)
    spacer_frame.grid(row=1, column=0)

    # Parking Grid Frame
    parking_frame = tk.Frame(root)
    parking_frame.grid(row=2, column=0, padx=10, pady=10)

    # Parking Grid
    parking_grid = [[False] * 10 for _ in range(3)]
    parking_spaces = []
    for i in range(3):
        row_spaces = []
        for j in range(10):
            frame = tk.Frame(
                parking_frame,
                width=50,
                height=50,
                bg="white",
                highlightbackground="black",
                highlightthickness=1
            )
            frame.grid(row=i, column=j, padx=5, pady=5)

            # Label each parking space
            label = tk.Label(frame, text=f"{i+1}-{j+1}", bg="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

            frame.bind("<Button-1>", toggle_parking)

            row_spaces.append(frame)

        parking_spaces.append(row_spaces)

    root.mainloop()


# In[ ]:




