import tkinter as tk
from tkinter import ttk
import pandas as pd

principal = 0
down_payment = 0

def calculate_monthly_payment(principal, down_payment, annual_interest_rate, loan_term, quarterly=False):
    if quarterly:
        n = loan_term * 4
        r = annual_interest_rate / 400  # Quarterly interest rate
    else:
        n = loan_term * 12
        r = annual_interest_rate / 1200  # Monthly interest rate

    loan_amount = principal - down_payment
    monthly_payment = loan_amount * r / (1 - (1 + r) ** -n)
    total_payment = 0
    payments = []

    for period in range(1, n + 1):
        interest_payment = loan_amount * r
        principal_payment = monthly_payment - interest_payment
        loan_amount -= principal_payment

        if period % 4 == 0 and quarterly:
            total_payment_period = monthly_payment
        else:
            total_payment_period = monthly_payment * 3 if quarterly else monthly_payment

        payments.append([period, interest_payment, principal_payment, total_payment_period])

        total_payment += total_payment_period

    return payments, total_payment

def calculate_button_clicked():
    global principal, down_payment, payments, total_payment
    principal = float(principal_entry.get())
    down_payment = float(down_payment_entry.get())
    annual_interest_rate = float(annual_interest_rate_entry.get())
    loan_term = int(loan_term_entry.get())
    quarterly = quarterly_checkbutton.get()

    payments, total_payment = calculate_monthly_payment(principal, down_payment, annual_interest_rate, loan_term, quarterly)

    df = pd.DataFrame(payments, columns=["Период", "Проценты", "Основной платеж", "Сумма платежа"])
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, df.to_string(index=False))
    result_text.insert(tk.END, "\nСумма всех основных платежей: {:.2f}\n".format(total_payment - principal + down_payment))
    result_text.insert(tk.END, "Сумма платежей по процентам (размер переплаты): {:.2f}".format(total_payment))

def extra_payment_button_clicked():
    global principal, down_payment, payments, total_payment
    extra_payment = float(extra_payment_entry.get())
    if extra_payment > 0:
        for i in range(len(payments)):
            if extra_payment <= 0:
                break
            if payments[i][3] > 0:
                principal_payment = min(payments[i][3], extra_payment)
                extra_payment -= principal_payment
                payments[i][2] += principal_payment
                payments[i][3] -= principal_payment

    df = pd.DataFrame(payments, columns=["Период", "Проценты", "Основной платеж", "Сумма платежа"])
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, df.to_string(index=False))
    result_text.insert(tk.END, "\nСумма всех основных платежей: {:.2f}\n".format(total_payment - principal + down_payment))
    result_text.insert(tk.END, "Сумма платежей по процентам (размер переплаты): {:.2f}".format(total_payment))

app = tk.Tk()
app.title("Платежи по кредиту")

frame = ttk.Frame(app)
frame.grid(row=0, column=0, padx=10, pady=10)

principal_label = ttk.Label(frame, text="Сумма покупки:")
principal_label.grid(row=0, column=0)
principal_entry = ttk.Entry(frame)
principal_entry.grid(row=0, column=1)

down_payment_label = ttk.Label(frame, text="Сумма первоначального платежа:")
down_payment_label.grid(row=1, column=0)
down_payment_entry = ttk.Entry(frame)
down_payment_entry.grid(row=1, column=1)

annual_interest_rate_label = ttk.Label(frame, text="Годовая процентная ставка:")
annual_interest_rate_label.grid(row=2, column=0)
annual_interest_rate_entry = ttk.Entry(frame)
annual_interest_rate_entry.grid(row=2, column=1)

loan_term_label = ttk.Label(frame, text="Срок кредита (в годах):")
loan_term_label.grid(row=3, column=0)
loan_term_entry = ttk.Entry(frame)
loan_term_entry.grid(row=3, column=1)

quarterly_checkbutton = tk.BooleanVar()
quarterly_checkbutton.set(False)
quarterly_checkbox = ttk.Checkbutton(frame, text="Платежи ежеквартально", variable=quarterly_checkbutton)
quarterly_checkbox.grid(row=4, column=0, columnspan=2)

calculate_button = ttk.Button(frame, text="Рассчитать", command=calculate_button_clicked)
calculate_button.grid(row=5, column=0, columnspan=2)

result_text = tk.Text(frame, height=10, width=40)
result_text.grid(row=6, column=0, columnspan=2)

extra_payment_label = ttk.Label(frame, text="Дополнительный платеж:")
extra_payment_label.grid(row=7, column=0)
extra_payment_entry = ttk.Entry(frame)
extra_payment_entry.grid(row=7, column=1)

extra_payment_button = ttk.Button(frame, text="Применить дополнительный платеж", command=extra_payment_button_clicked)
extra_payment_button.grid(row=8, column=0, columnspan=2)

payments, total_payment = [], 0

app.mainloop()
