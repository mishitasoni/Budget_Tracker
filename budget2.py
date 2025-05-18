import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt

# === Connect to MySQL Database ===
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kishmish2@",  # Replace with your password
        database="budget_db"
    )

# === Add Expense Logic ===
def add_expense_gui():
    date = date_entry.get()
    category = category_entry.get()
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Amount must be a number.")
        return

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Invalid input", "Date must be in YYYY-MM-DD format.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (%s, %s, %s)", 
                   (date, category, amount))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Expense added successfully!")

# === Set Budget Logic ===
def set_budget_gui():
    month = budget_month_entry.get()
    try:
        amount = float(budget_amount_entry.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Budget must be a number.")
        return

    try:
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        messagebox.showerror("Invalid input", "Month must be in YYYY-MM format.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO budget (month, amount) VALUES (%s, %s)", (month, amount))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Budget set successfully!")

# === View Summary Logic ===
def view_summary_gui():
    month = summary_month_entry.get()

    try:
        datetime.strptime(month, '%Y-%m')
    except ValueError:
        messagebox.showerror("Invalid input", "Month must be in YYYY-MM format.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) 
        FROM expenses 
        WHERE DATE_FORMAT(date, '%Y-%m') = %s 
        GROUP BY category
    """, (month,))
    data = cursor.fetchall()

    cursor.execute("SELECT amount FROM budget WHERE month = %s", (month,))
    budget = cursor.fetchone()
    budget_amount = budget[0] if budget else 0
    conn.close()

    total = sum([row[1] for row in data])
    result_text = f"Month: {month}\nTotal Expenses: ₹{total}\nBudget: ₹{budget_amount}\nRemaining: ₹{budget_amount - total:.2f}"

    messagebox.showinfo("Summary", result_text)

    if data:
        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]
        plt.figure(figsize=(6,6))
        
        plt.pie(amounts, labels=categories, autopct='%1.1f%%',shadow='True')
        plt.title(f"Expenses by Category - {month}")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses found for this month.")

# === GUI Setup ===
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("420x620")
root.configure(bg="#ffe6f0")  # 💗 Soft pink background

# === ttk Styling ===
style = ttk.Style()
style.theme_use('clam')  # Theme that allows color customization

# Apply custom frame and label styles with white backgrounds
style.configure("Custom.TLabelframe", background="#ffffff", borderwidth=1, relief="solid")
style.configure("Custom.TLabelframe.Label", background="#ffffff", font=("Segoe UI", 12, "bold"))
style.configure("Custom.TLabel", background="#ffffff", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))

# === Frame Factory ===
def make_section(title):
    frame = ttk.LabelFrame(root, text=title, style="Custom.TLabelframe", padding=10)
    frame.pack(fill="both", expand=False, padx=15, pady=10)
    return frame

# === Add Expense Section ===
expense_frame = make_section("Add Expense")

ttk.Label(expense_frame, text="Date (YYYY-MM-DD):", style="Custom.TLabel").grid(row=0, column=0, sticky="e", pady=5)
date_entry = ttk.Entry(expense_frame)
date_entry.grid(row=0, column=1, pady=5)

ttk.Label(expense_frame, text="Category:", style="Custom.TLabel").grid(row=1, column=0, sticky="e", pady=5)
category_entry = ttk.Entry(expense_frame)
category_entry.grid(row=1, column=1, pady=5)

ttk.Label(expense_frame, text="Amount:", style="Custom.TLabel").grid(row=2, column=0, sticky="e", pady=5)
amount_entry = ttk.Entry(expense_frame)
amount_entry.grid(row=2, column=1, pady=5)

ttk.Button(expense_frame, text="Add Expense", command=add_expense_gui).grid(row=3, column=0, columnspan=2, pady=10)

# === Set Budget Section ===
budget_frame = make_section("Set Monthly Budget")

ttk.Label(budget_frame, text="Month (YYYY-MM):", style="Custom.TLabel").grid(row=0, column=0, sticky="e", pady=5)
budget_month_entry = ttk.Entry(budget_frame)
budget_month_entry.grid(row=0, column=1, pady=5)

ttk.Label(budget_frame, text="Budget Amount:", style="Custom.TLabel").grid(row=1, column=0, sticky="e", pady=5)
budget_amount_entry = ttk.Entry(budget_frame)
budget_amount_entry.grid(row=1, column=1, pady=5)

ttk.Button(budget_frame, text="Set Budget", command=set_budget_gui).grid(row=2, column=0, columnspan=2, pady=10)

# === View Summary Section ===
summary_frame = make_section("View Monthly Summary")

ttk.Label(summary_frame, text="Month (YYYY-MM):", style="Custom.TLabel").grid(row=0, column=0, sticky="e", pady=5)
summary_month_entry = ttk.Entry(summary_frame)
summary_month_entry.grid(row=0, column=1, pady=5)

ttk.Button(summary_frame, text="View Summary", command=view_summary_gui).grid(row=1, column=0, columnspan=2, pady=10)

# === Start App ===
root.mainloop()
