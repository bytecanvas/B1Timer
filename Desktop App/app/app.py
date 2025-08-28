import tkinter as tk
from tkinter import messagebox
import time
import pygame  # Import pygame for MP3 sound support

# Main Application Class
class TimerApp:
    def __init__(self, root):
        # Initialize Pygame mixer
        pygame.mixer.init()

        self.root = root
        self.root.title("German B1 Exam Timer")
        self.root.geometry("340x514")  # Approximate 9.5 cm x 14.5 cm in pixels
        self.root.config(bg="#2C3E50")  # Darker background color for the window

        # Set the icon for the window
        try:
            self.root.iconbitmap("app_icon.ico")  # Replace with your .ico file path
        except Exception as e:
            print("Icon could not be loaded:", e)

        self.running = False
        self.paused = False
        self.time_left = 0
        self.start_time = None
        self.selected_module = tk.StringVar()
        self.selected_module.set("Lesen")

        # Fonts and Colors
        self.font = ("Arial", 12, "bold")
        self.timer_font = ("Arial", 20, "bold")
        self.button_font = ("Arial", 10, "normal")
        self.bg_color = "#2C3E50"  # Dark background
        self.text_color = "#ECF0F1"  # Light text color for readability

        # Title Label - Centered
        self.title_label = tk.Label(root, text="German B1 Exam Timer", font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        self.title_label.pack(pady=10)

        # Timer Label
        self.timer_label = tk.Label(root, text="00:00", font=self.timer_font, width=10, bg=self.bg_color, fg=self.text_color)
        self.timer_label.pack(pady=20)

        # Timer Modules
        self.modules = {
            "Lesen": 65 * 60,    # 65 minutes
            "Horen": 40 * 60,    # 40 minutes
            "Schreiben": 60 * 60, # 60 minutes
            "Sprechen": 15 * 60, # 15 minutes
        }

        # Dropdown Menu to select the module
        self.module_menu = tk.OptionMenu(root, self.selected_module, *self.modules.keys(), command=self.update_timer_for_module)
        self.module_menu.config(font=self.button_font)
        self.module_menu.pack(pady=10)

        # Buttons Layout
        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(pady=20)

        # Row 1: Start and Stop
        self.start_button = tk.Button(button_frame, text="Start", width=12, font=self.button_font, command=self.start_timer, bg="#B2FF59", fg="black", relief="flat", bd=5)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop", width=12, font=self.button_font, command=self.stop_timer, bg="#FF5252", fg="black", relief="flat", bd=5)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        # Row 2: Pause and Reset
        self.pause_button = tk.Button(button_frame, text="Pause", width=12, font=self.button_font, command=self.pause_timer, bg="#FFC107", fg="black", relief="flat", bd=5)
        self.pause_button.grid(row=1, column=0, padx=5, pady=5)

        self.reset_button = tk.Button(button_frame, text="Reset", width=12, font=self.button_font, command=self.reset_timer, bg="#9E9E9E", fg="black", relief="flat", bd=5)
        self.reset_button.grid(row=1, column=1, padx=5, pady=5)

        # Custom Timer Section
        self.custom_minutes_label = tk.Label(root, text="Minutes:", font=self.font, bg=self.bg_color, fg=self.text_color)
        self.custom_minutes_label.pack(pady=5)
        
        self.custom_minutes_entry = tk.Entry(root, width=5, font=self.font)
        self.custom_minutes_entry.pack(pady=5)

        self.set_custom_button = tk.Button(root, text="Set Custom Timer", width=15, font=self.button_font, command=self.set_custom_timer, bg="#8BC34A", fg="black", relief="flat", bd=5)
        self.set_custom_button.pack(pady=10)

        self.update_timer()

    # Automatically update the timer when a new module is selected
    def update_timer_for_module(self, selection):
        self.time_left = self.modules[selection]
        self.start_time = None
        self.update_timer()

    # Start Timer (Initial start or Resume after Pause)
    def start_timer(self):
        if self.paused:
            self.start_time = time.time() - self.time_left
            self.paused = False
            self.running = True
            self.update_timer()
        else:
            selected_module = self.selected_module.get()
            self.time_left = self.modules[selected_module]
            self.start_time = time.time()
            self.running = True
            self.update_timer()

    # Pause Timer
    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused = True

    # Reset Timer
    def reset_timer(self):
        # Reset to the selected module's time
        selected_module = self.selected_module.get()
        self.time_left = self.modules[selected_module]
        self.start_time = None
        self.running = False
        self.paused = False
        self.update_timer()

    # Stop Timer
    def stop_timer(self):
        self.running = False
        self.time_left = 0
        self.update_timer()

    # Set Custom Timer (with only minutes input)
    def set_custom_timer(self):
        try:
            minutes = int(self.custom_minutes_entry.get())
            if minutes < 0:
                raise ValueError("Invalid time input")
            self.time_left = minutes * 60
            self.start_time = time.time()
            self.running = True
            self.update_timer()
            self.paused = False
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of minutes.")

    # Play MP3 sound on completion and loop it once
    def play_sound(self):
        pygame.mixer.music.load("alarm.mp3")  # Replace with your MP3 file path
        pygame.mixer.music.play(loops=0, fade_ms=0)  # Play the sound once

    # Stop sound (if user stops or resets)
    def stop_sound(self):
        pygame.mixer.music.stop()

    # Update Timer Display
    def update_timer(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            remaining_time = self.time_left - elapsed_time
            if remaining_time <= 0:
                self.running = False
                self.time_left = 0
                self.stop_sound()  # Stop sound when the timer is done
                # Popup message and play the sound only after the timer ends
                self.play_sound()  
                self.show_popup()
            else:
                minutes = int(remaining_time // 60)
                seconds = int(remaining_time % 60)
                self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        elif not self.running and not self.paused:
            self.timer_label.config(text="00:00")

        self.root.after(1000, self.update_timer)  # Update every second

    # Display the messagebox and stop sound after it's closed
    def show_popup(self):
        # Show message box, and stop sound after user closes it
        messagebox.showinfo("Time's Up!", "The time for this section is over!")
        self.stop_sound()  # Stop the sound when the popup is closed

# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
