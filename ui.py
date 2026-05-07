import tkinter as tk
from tkinter import Menu, Tk, messagebox, simpledialog

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")  # Set Tkinter backend

import openmeteoToCsv as meteoCSV


def exitApp():
    root.quit()


def printAbout():
    with open("aboutus.txt", "r") as file:
        aboutUs = file.read()
    messagebox.showinfo(title="About this Project", message=f"{aboutUs}")


def createLoc():
    new_long = simpledialog.askfloat(
        title="Enter New Town Coordinates",
        prompt="Gimme the longitude of the new town you're looking for please!",
    )
    new_lat = simpledialog.askfloat(
        title="Enter New Town Coordinates",
        prompt="Gimme the latitute of the new town you're looking for please!",
    )
    new_name = simpledialog.askstring(
        title="Name the New Town!",
        prompt="Enter the name of this new town! Remember, this is case sensitive so make sure you spell it right!",
    )
    if new_lat and new_long and new_name is not None:
        meteoCSV.fetchData(new_lat, new_long, new_name)


def openLoc():
    # Use a text box to gather user input
    town_name = simpledialog.askstring(
        title="Input Location Name Below Please:",
        prompt="Please enter the name of the town you want to see weather data for. Please type the name of just the town, while using proper capitalization :)",
    )

    # Exit if user cancels the dialog
    if not town_name:
        return

    try:
        # Attempt to read the CSV file
        filename = f"Hourly_Weather_Data_{town_name}.csv"
        weather_dataframe = pd.read_csv(filename)

        messagebox.showinfo(
            title="Success!",
            message=f"Weather data for {town_name} loaded successfully!",
        )

        # Prepare data: Create Hour column (1-24)
        # Note: Ensure your dataframe has enough rows or handle mismatched lengths
        weather_dataframe["Hour"] = np.arange(1, 25)

        # Create the figure and a grid of subplots (2 rows, 3 columns)
        fig = Figure(figsize=(8, 6), dpi=100)
        # This creates a 2x3 grid of axes objects
        axes = fig.subplots(2, 3)
        fig.suptitle(f"Weather data in {town_name}")

        # Plotting data
        # Row 0
        axes[0, 0].plot(weather_dataframe["Hour"], weather_dataframe["temperature_2m"])
        axes[0, 0].set_title("Temperature (F)")

        axes[0, 1].plot(
            weather_dataframe["Hour"], weather_dataframe["relative_humidity_2m"]
        )
        axes[0, 1].set_title("Relative Humidity")

        axes[0, 2].plot(
            weather_dataframe["Hour"], weather_dataframe["precipitation_probability"]
        )
        axes[0, 2].set_title("Precipitation Probability")

        # Row 1
        axes[1, 0].plot(weather_dataframe["Hour"], weather_dataframe["precipitation"])
        axes[1, 0].set_title("Precipitation (in)")

        axes[1, 1].plot(weather_dataframe["Hour"], weather_dataframe["wind_speed_10m"])
        axes[1, 1].set_title("Wind Speed (mph)")

        axes[1, 2].plot(weather_dataframe["Hour"], weather_dataframe["uv_index"])
        axes[1, 2].set_title("UV Index")

        # Adjust layout to prevent overlap
        fig.tight_layout()

        # Embed figure in Tkinter
        # We pack the widget into the root window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Optional: Add a close button or destroy old canvas if re-opening

    except FileNotFoundError:
        messagebox.showerror(
            title="File Not Found",
            message=f"Could not find the file: Hourly_Weather_Data_{town_name}.csv\nPlease check the spelling and try again.",
        )
    except KeyError as e:
        # Handles cases where a column name (e.g., "temperature_2m") doesn't exist
        messagebox.showerror(
            title="Data Error",
            message=f"The file is missing a required column: {e}\nCheck your CSV headers.",
        )
    except Exception as e:
        # Catch-all for any other unexpected errors, but prints the error to console for debugging
        print(f"An unexpected error occurred: {e}")
        messagebox.showerror(
            title="Unexpected Error",
            message=f"Something went wrong while processing the data: {str(e)}",
        )


root = Tk()
root.title("Buddies Weathinator 9000")

# Init. window geometry
window_width = 800
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Input Window Icon depending on if machine is running Windows or Linux/MacOS
if root.tk.call("tk", "windowingsystem") == "win32":
    root.iconbitmap("./assets/kittyicon.ico")  # b MUST BE ICO FILE
else:
    try:
        photo = tk.PhotoImage(file="./assets/kittyiconpng.png")
        root.iconphoto(False, photo)
    except tk.TclError:
        print("Icon file not found :(")

# Create the menu with necessary func.
menubar = Menu(root)
root.config(menu=menubar)

# Creating File Menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New Location")  # Run fn. to enter coords for new location
file_menu.add_command(label="Open Location", command=openLoc)
file_menu.add_command(label="Close Location")
file_menu.add_separator()

# Exit menu
file_menu.add_command(label="Exit", command=exitApp)

# Add filemenu to cascade
menubar.add_cascade(label="File", menu=file_menu)

# Repeat steps for the help menu
help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="About...", command=printAbout)
menubar.add_cascade(label="Help", menu=help_menu)

# Run the app
root.mainloop()

# if __name__ == "__main__":
#     main()
