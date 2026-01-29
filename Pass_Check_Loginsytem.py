import tkinter as tk
from tkinter import ttk, messagebox
import os

# ---------------- CONFIG ----------------
FILE = "users.txt"
BG_COLOR = "#f4f6f8"
TEXT_COLOR = "#333333"

# ---------------- FILE LOGIC ----------------
def user_exists(username):
    if not os.path.exists(FILE):
        return False
    with open(FILE, "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if u == username:
                return True
    return False

def save_user(username, password):
    with open(FILE, "a") as f:
        f.write(f"{username},{password}\n")

def validate_login(username, password):
    with open(FILE, "r") as f:
        for line in f:
            u, p = line.strip().split(",")
            if u == username and p == password:
                return True
    return False

# ---------------- PASSWORD STRENGTH ----------------
def password_strength(password):
    has_u = has_l = has_d = has_s = False

    for ch in password:
        if ch.isupper():
            has_u = True
        elif ch.islower():
            has_l = True
        elif ch.isdigit():
            has_d = True
        else:
            has_s = True

    score = 0
    if len(password) >= 8: score += 25
    if has_u: score += 25
    if has_l: score += 25
    if has_d or has_s: score += 25

    return score

# ---------------- FRAME SWITCH ----------------
def show_login():
    checker_frame.pack_forget()
    login_frame.pack(pady=40)

def show_checker():
    login_frame.pack_forget()
    checker_frame.pack(pady=30)

# ---------------- LOGIN / REGISTER ----------------
def login():
    u = user_entry.get()
    p = pass_entry.get()

    if not os.path.exists(FILE):
        messagebox.showerror("Error", "No users registered yet")
        return

    if validate_login(u, p):
        messagebox.showinfo("Success", f"Welcome {u} 👋")
        show_checker()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def register():
    u = user_entry.get()
    p = pass_entry.get()

    if u == "" or p == "":
        messagebox.showerror("Error", "All fields required")
        return

    if user_exists(u):
        messagebox.showerror("Error", "User already exists")
        return

    if password_strength(p) < 75:
        messagebox.showwarning("Weak Password",
                               "Use uppercase, lowercase, digit & symbol")
        return

    save_user(u, p)
    messagebox.showinfo("Success", "Registration successful 🎉")

# ---------------- PASSWORD CHECKER ----------------
def check_password():
    p = check_entry.get()
    score = password_strength(p)
    progress["value"] = score

    if score == 100:
        result_label.config(text="Strong Password 💪", fg="green")
    elif score >= 50:
        result_label.config(text="Medium Password 🙂", fg="orange")
    else:
        result_label.config(text="Weak Password ❌", fg="red")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Login + Password Checker")
root.geometry("520x520")
root.configure(bg=BG_COLOR)
root.resizable(False, False)
root.eval("tk::PlaceWindow . center")

# -------- Progress Bar Style --------
style = ttk.Style()
style.theme_use("default")
style.configure("TProgressbar", thickness=12)

# ---------------- LOGIN FRAME ----------------
login_frame = tk.Frame(root, bg=BG_COLOR)
login_frame.pack(pady=40)

tk.Label(
    login_frame,
    text="Login / Register",
    font=("Segoe UI", 20, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
).pack(pady=20)

tk.Label(login_frame, text="Username", bg=BG_COLOR,
         fg=TEXT_COLOR).pack()
user_entry = tk.Entry(login_frame, width=32,
                      font=("Segoe UI", 11), bd=1, relief="solid")
user_entry.pack(pady=8)

tk.Label(login_frame, text="Password", bg=BG_COLOR,
         fg=TEXT_COLOR).pack()
pass_entry = tk.Entry(login_frame, show="*", width=32,
                      font=("Segoe UI", 11), bd=1, relief="solid")
pass_entry.pack(pady=8)

tk.Button(
    login_frame,
    text="Login",
    width=24,
    font=("Segoe UI", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    relief="flat",
    command=login
).pack(pady=8)

tk.Button(
    login_frame,
    text="Register",
    width=24,
    font=("Segoe UI", 11, "bold"),
    bg="#2196F3",
    fg="white",
    relief="flat",
    command=register
).pack(pady=5)

# ---------------- CHECKER FRAME ----------------
checker_frame = tk.Frame(root, bg=BG_COLOR)

tk.Label(
    checker_frame,
    text="Password Strength Checker",
    font=("Segoe UI", 20, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
).pack(pady=20)

tk.Label(checker_frame, text="Enter Password",
         bg=BG_COLOR, fg=TEXT_COLOR).pack()

check_entry = tk.Entry(
    checker_frame,
    show="*",
    width=32,
    font=("Segoe UI", 11),
    bd=1,
    relief="solid"
)
check_entry.pack(pady=8)

progress = ttk.Progressbar(checker_frame, length=260, maximum=100)
progress.pack(pady=15)

tk.Button(
    checker_frame,
    text="Check Password",
    width=24,
    font=("Segoe UI", 11, "bold"),
    bg="#9C27B0",
    fg="white",
    relief="flat",
    command=check_password
).pack(pady=10)

result_label = tk.Label(
    checker_frame,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg=BG_COLOR
)
result_label.pack(pady=10)

tk.Button(
    checker_frame,
    text="Logout",
    width=24,
    font=("Segoe UI", 11, "bold"),
    bg="#f44336",
    fg="white",
    relief="flat",
    command=show_login
).pack(pady=20)

root.mainloop()
