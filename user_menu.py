import tkinter as tk
import mysql.connector as sql
from register import Register
from forget_password import ForgetPassword

class UserMenu:
    def __init__(self, window):
        self.window = window
        self.logged_in = False
        self.update_user_icon_callback = None
        self.update_user_data_callback = None

    def show_user_menu(self, event):
        self.user_menu_window = tk.Toplevel(self.window)
        self.user_menu_window.title("Log in")
        self.user_menu_window.iconbitmap('images/ch.ico')

        # Center the window on the screen
        window_width = 300
        window_height = 200
        screen_width = self.user_menu_window.winfo_screenwidth()
        screen_height = self.user_menu_window.winfo_screenheight()

        x_position = int((screen_width / 2) - (window_width / 2))
        y_position = int((screen_height / 2) - (window_height / 2))

        self.user_menu_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create a frame to contain the widgets
        login_frame = tk.Frame(self.user_menu_window)
        login_frame.pack(pady=(40, 0))

        # Username and password labels and entry fields with reduced padx
        username_label = tk.Label(login_frame, text="Username:")
        username_label.grid(row=0, column=0, pady=(0, 5), sticky=tk.W)

        self.username_entry = tk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, pady=(0, 5), padx=(2, 0), sticky=tk.W)

        password_label = tk.Label(login_frame, text="Password:")
        password_label.grid(row=1, column=0, pady=(5, 0), sticky=tk.W)

        self.password_entry = tk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=(5, 0), padx=(2, 0), sticky=tk.W)

        # Create a frame to contain the buttons
        button_frame = tk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Sign In button
        self.sign_in_button = tk.Button(
            button_frame,
            text="Sign In",
            command=self.login
        )
        self.sign_in_button.grid(row=0, column=0, padx=(0, 10), pady=(0, 5))

        # Forget Password button
        self.forget_password_button = tk.Button(
            button_frame,
            text="Forget Password",
            command=self.forget_password
        )
        self.forget_password_button.grid(row=1, column=0, columnspan=2, pady=(5, 0))

        # Register button
        self.register_button = tk.Button(
            button_frame,
            text="Register",
            command=self.register
        )
        self.register_button.grid(row=0, column=1, padx=(10, 0), pady=(0, 5))

    def login(self):
        # Call the signin function with entered username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.signin(username, password)

        if success != False:
            self.logged_in = True
            print("Logged in")
            if self.update_user_icon_callback:  # Check if the callback is assigned
                self.update_user_icon_callback()  # Call the callback function
            self.user_menu_window.destroy()
            if self.update_user_data_callback:
                self.update_user_data_callback(username)
            return success
        else:
            error_msg = "Invalid username or password."
            tk.messagebox.showerror("Error", error_msg)
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            return None


    def signup(self):
        print("Sign up")

    # def sidebar_action(self, button_text):
    #     print(f"Clicked {button_text}")

    def forget_password(self):
        forget_password = ForgetPassword(self.user_menu_window)
        forget_password.show_forget_password_window()

    def register(self):
        Register(self.user_menu_window)

    def is_logged_in(self):
        return self.logged_in

    def signin(self, username, password):
        db = sql.connect(host="localhost", user="root", password="root", database="comics", port=3306, autocommit=True)
        cursor = db.cursor(buffered=True)
        data = (username, password)
        cursor.execute("SELECT * from users WHERE username = %s and password = %s", data)
        result = cursor.fetchone()

        # Close the database connection
        cursor.close()
        db.close()

        if result:
            return result[0]  # Return the username
        else:
            return False
