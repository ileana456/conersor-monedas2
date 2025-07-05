import tkinter as tk
from tkinter import ttk

# Tasas de cambio fijas (sin duplicados)
exchange_rates = {
    ("USD", "EUR"): 0.89,
    ("USD", "MXN"): 17.14,
    ("USD", "GBP"): 0.78,
    ("USD", "JPY"): 157.30,
    ("USD", "CAD"): 1.36,
    ("USD", "BRL"): 5.42,
    ("USD", "CHF"): 0.89,
    ("EUR", "USD"): 1 / 0.89,
    ("EUR", "MXN"): 19.25,
    ("EUR", "GBP"): 0.87,
    ("EUR", "JPY"): 170.50,
    ("EUR", "CAD"): 1.52,
    ("EUR", "BRL"): 6.10,
    ("EUR", "CHF"): 0.98,
    ("MXN", "USD"): 1 / 17.14,
    ("MXN", "EUR"): 1 / 19.25,
    ("GBP", "USD"): 1 / 0.78,
    ("GBP", "EUR"): 1 / 0.87,
    ("JPY", "USD"): 1 / 157.30,
    ("JPY", "EUR"): 1 / 170.50,
    ("CAD", "USD"): 1 / 1.36,
    ("CAD", "EUR"): 1 / 1.52,
    ("BRL", "USD"): 1 / 5.42,
    ("BRL", "EUR"): 1 / 6.10,
    ("CHF", "USD"): 1 / 0.89,
    ("CHF", "EUR"): 1 / 0.98,
}

monedas = ["USD", "EUR", "MXN", "GBP", "JPY", "CAD", "BRL", "CHF"]

class ConversorDeMonedas:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Monedas")
        self.root.configure(bg="#B95013")
        self.input_value = ""

        self.from_currency = tk.StringVar(value="USD")
        self.to_currency = tk.StringVar(value="EUR")

        self.frame = tk.Frame(self.root, bg="#219464")
        self.frame.pack(expand=True)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Moneda origen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.from_combo = ttk.Combobox(self.frame, textvariable=self.from_currency, values=monedas, state="readonly")
        self.from_combo.grid(row=0, column=1, pady=5)
        self.from_combo.bind("<<ComboboxSelected>>", lambda e: self.update_rate_label())

        self.input_entry = tk.Entry(self.frame, font=("Arial", 18), justify="right", width=10)
        self.input_entry.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Label(self.frame, text="Moneda destino").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.to_combo = ttk.Combobox(self.frame, textvariable=self.to_currency, values=monedas, state="readonly")
        self.to_combo.grid(row=2, column=1, pady=5)
        self.to_combo.bind("<<ComboboxSelected>>", lambda e: self.update_rate_label())

        self.output_entry = tk.Entry(self.frame, font=("Arial", 18), justify="right", width=10)
        self.output_entry.grid(row=3, column=0, columnspan=2, pady=5)

        self.rate_label = tk.Label(self.frame, text="", bg="#6A0DAD", fg="white")
        self.rate_label.grid(row=4, column=0, columnspan=2, pady=5)
        self.update_rate_label()

        keypad_frame = tk.Frame(self.frame, bg="#6A0DAD")
        keypad_frame.grid(row=5, column=0, columnspan=2)

        buttons = [
            "7", "8", "9", "C",
            "4", "5", "6", "←",
            "1", "2", "3", "=",
            "0", "00", ".", "↔"
        ]

        row = 0
        col = 0
        for button in buttons:
            action = lambda x=button: self.click(x)
            tk.Button(
                keypad_frame, text=button, width=5, height=2,
                command=action, bg="#00BFFF", fg="white", font=("Arial", 12),
                activebackground="#1E90FF", bd=0
            ).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click(self, key):
        if key == "C":
            self.input_value = ""
            self.input_entry.delete(0, tk.END)
            self.output_entry.delete(0, tk.END)
        elif key == "←":
            self.input_value = self.input_value[:-1]
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.input_value)
        elif key == "=":
            self.convert()
        elif key == "↔":
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            self.from_currency.set(to_curr)
            self.to_currency.set(from_curr)
            self.update_rate_label()
        else:
            # Solo permitir números y un punto decimal
            if key == "." and "." in self.input_value:
                return
            if key not in "0123456789." and key != "00":
                return
            self.input_value += key
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.input_value)

    def convert(self):
        try:
            amount = float(self.input_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()
            if from_curr == to_curr:
                converted = amount
                rate = 1
            else:
                rate = exchange_rates.get((from_curr, to_curr))
                if rate is None:
                    self.output_entry.delete(0, tk.END)
                    self.output_entry.insert(0, "No disponible")
                    return
                converted = round(amount * rate, 2)

            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, f"{converted}")
            self.rate_label.config(text=f"Tasa: 1 {from_curr} = {round(rate, 4)} {to_curr}")
        except Exception:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, "Error")

    def update_rate_label(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        if from_curr == to_curr:
            self.rate_label.config(text=f"Tasa: 1 {from_curr} = 1 {to_curr}")
        else:
            rate = exchange_rates.get((from_curr, to_curr))
            if rate:
                self.rate_label.config(text=f"Tasa: 1 {from_curr} = {round(rate, 4)} {to_curr}")
            else:
                self.rate_label.config(text="Tasa no disponible")

# Ejecutar aplicación
root = tk.Tk()
root.geometry("600x450")
app = ConversorDeMonedas(root)
root.mainloop()