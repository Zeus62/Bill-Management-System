from tkinter import *
from tkinter import messagebox
from database import Database
from datetime import datetime

class BillApp:

    def __init__(self):
        self.root = Tk()
        self.root.title("Bill Management")
        self.root.resizable(False, False)
        self.root.geometry("1300x700")

        # Create a database instance
        self.db = Database()

        # Create header
        header_label = Label(self.root, text="BILL MANAGEMENT", bg="navy", fg="white",
                             font=("Helvetica", 30, "bold"), pady=10)
        header_label.pack(fill=X)

        # GUI layout setup (Menu, Order, Bill sections)
        self.create_menu_section()
        self.create_order_section()
        self.create_bill_section()

        # Start Tkinter event loop
        self.root.mainloop()

    def create_menu_section(self):
        """Create menu section with available items."""
        menu_frame = Frame(self.root, bg="lightblue", bd=5, relief=RIDGE)
        menu_frame.place(x=10, y=80, width=280, height=600)
        menu_title = Label(menu_frame, text="Menu", font=("Helvetica", 24, "bold"),
                           fg="darkblue", bg="lightblue")
        menu_title.pack(side=TOP, fill=X)
        # List of items and their variables
        self.items = [
            ("Dosa", 3.00),
            ("Cookies", 1.50),
            ("Tea", 0.50),
            ("Coffee", 2.00),
            ("Juice", 1.00),
            ("Pancakes", 1.25),
            ("Eggs", 0.35)
        ]

        for item, price in self.items:
            item_frame = Frame(menu_frame, bg="lightblue")
            item_frame.pack(fill=X, padx=20, pady=2)
            Label(item_frame, text=item, font=("Arial", 16), bg="lightblue", anchor='w').pack(side=LEFT)
            Label(item_frame, text=f"${price:.2f}", font=("Arial", 16), bg="lightblue", anchor='e').pack(side=RIGHT)

    def create_order_section(self):
        """Create order section with input fields."""
        order_frame = Frame(self.root, bd=5, relief=RIDGE)
        order_frame.place(x=300, y=80, width=380, height=600)

        self.entries = {}
        for i, (item_name, _) in enumerate(self.items):
            Label(order_frame, font=("Arial", 18), text=item_name, fg="black", padx=10, pady=5).grid(row=i, column=0, sticky='w')
            self.entries[item_name] = StringVar()
            Entry(order_frame, font=("Arial", 16), textvariable=self.entries[item_name], bd=5, width=10).grid(row=i, column=1, padx=10, pady=5)

        # Create buttons
        btn_frame = Frame(order_frame)
        btn_frame.grid(row=len(self.items), column=0, columnspan=2, pady=20)

        Button(btn_frame, text="Reset", font=("Arial", 16, "bold"), bg="lightgray", fg="black", width=12, command=self.reset).grid(row=0, column=0, padx=10, pady=5)
        Button(btn_frame, text="Total", font=("Arial", 16, "bold"), bg="lightgreen", fg="black", width=12, command=self.calculate_total).grid(row=0, column=1, padx=10, pady=5)
        Button(btn_frame, text="Show Orders", font=("Arial", 16, "bold"), bg="lightyellow", fg="black", width=12, command=self.db.show_orders).grid(row=1, column=0, padx=10, pady=5)

    def create_bill_section(self):
        """Create bill display area."""
        bill_frame = Frame(self.root, bd=5, relief=RIDGE)
        bill_frame.place(x=700, y=80, width=600, height=600)
        Label(bill_frame, text="Bill", font=("Helvetica", 24, "bold"), bg="lightyellow").pack(side=TOP, fill=X)
        self.bill_text = Text(bill_frame, font=("Courier New", 14), bg="white")
        self.bill_text.pack(fill=BOTH, expand=True)

    def reset(self):
        """Clear all fields."""
        for var in self.entries.values():
            var.set("")
        self.bill_text.delete(1.0, END)

    def calculate_total(self):
        """Calculate and display total bill."""
        total = 0.0
        self.bill_text.delete(1.0, END)
        self.bill_text.insert(END, f"{'Item':<15}{'Qty':<10}{'Price':<15}{'Total':<10}\n")
        self.bill_text.insert(END, "-" * 53 + "\n")

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for item, price in self.items:
            qty = self.entries[item].get()
            if qty and qty.isdigit():
                qty = int(qty)
                amount = qty * price
                total += amount
                self.bill_text.insert(END, f"{item:<15}{qty:<10}{price:<15.2f}{amount:<10.2f}\n")
                self.db.add_order(item, qty, price, amount, current_time)

        self.bill_text.insert(END, "-" * 53 + "\n")
        self.bill_text.insert(END, f"{'Total Amount:':<40}${total:.2f}\n\n")
        self.bill_text.insert(END, "Thank you for visiting us!")

    def run(self):
        """Run the application."""
        self.root.mainloop()
