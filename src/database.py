import sqlite3
from tkinter import Toplevel, Text, Scrollbar, RIGHT, Y, BOTH, END

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bills.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS orders
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           item TEXT, quantity INTEGER, price REAL, total REAL, date DATETIME)''')
        self.conn.commit()

    def add_order(self, item, quantity, price, total, date):
        """Insert order into database."""
        self.c.execute("INSERT INTO orders (item, quantity, price, total, date) VALUES (?, ?, ?, ?, ?)",
                       (item, quantity, price, total, date))
        self.conn.commit()

    def show_orders(self):
        """Display all orders in a new window."""
        # Create new window for orders
        orders_window = Toplevel()
        orders_window.title("All Orders")
        orders_window.geometry("800x600")

        # Add scrollbar
        scroll = Scrollbar(orders_window)
        scroll.pack(side=RIGHT, fill=Y)

        # Create text area for orders
        orders_text = Text(orders_window, font=("Courier New", 12), bg="white", yscrollcommand=scroll.set)
        orders_text.pack(fill=BOTH, expand=True)
        scroll.config(command=orders_text.yview)

        self.c.execute("SELECT DISTINCT date FROM orders ORDER BY date DESC")
        dates = self.c.fetchall()

        if not dates:
            orders_text.insert(END, "No orders found in the database.")
            return

            # Display each order
        for date in dates:
            orders_text.insert(END, "\n" + "=" * 70 + "\n")
            orders_text.insert(END, f"Date: {date[0]}\n")
            orders_text.insert(END, "=" * 70 + "\n\n")
            orders_text.insert(END, f"{'Item':<15}{'Qty':<10}{'Price':<10}{'Total':<10}\n")
            orders_text.insert(END, "-" * 45 + "\n")
            # Get items for this order
            self.c.execute("""
                    SELECT item, quantity, price, total 
                    FROM orders 
                    WHERE date = ?
                    ORDER BY id""", (date[0],))

            items = self.c.fetchall()
            total_bill = 0

            # Display items and calculate total
            for item in items:
                orders_text.insert(END, f"{item[0]:<15}{item[1]:<10}{item[2]:<10.2f}{item[3]:<10.2f}\n")
                total_bill += item[3]

            # Display Total
            orders_text.insert(END, "-" * 45 + "\n")
            orders_text.insert(END, f"{'Total Bill:':<35}${total_bill:.2f}\n")
            orders_text.insert(END, "\n" + "Thank you for visiting us!" + "\n\n")

        orders_text.config(state="disabled")

    def close(self):
        """Close database connection."""
        self.conn.close()
