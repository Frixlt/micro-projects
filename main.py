import tkinter as tk

def calculate_payments():
    principal = float(principal_entry.get())
    down_payment = float(down_payment_entry.get())
    interest_rate = float(interest_rate_entry.get()) / 100
    loan_term = int(loan_term_entry.get())
    
    loan_amount = principal - down_payment
    monthly_interest_rate = interest_rate / 12
    num_payments = loan_term * 12
    monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    
    result_label.config(text=f"Ежемесячный платеж: {monthly_payment:.2f}")
    
    payment_schedule.delete(1.0, tk.END)
    balance = loan_amount
    for month in range(1, num_payments + 1):
        interest_payment = balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        payment_schedule.insert(tk.END, f"Месяц {month}: Основной платеж: {principal_payment:.2f}, Платеж по процентам: {interest_payment:.2f}, Остаток долга: {balance:.2f}\n")

# Создание графического интерфейса
app = tk.Tk()
app.title("Платежи по кредиту")

principal_label = tk.Label(app, text="Цена покупки:")
principal_label.pack()
principal_entry = tk.Entry(app)
principal_entry.pack()

down_payment_label = tk.Label(app, text="Первоначальный платеж:")
down_payment_label.pack()
down_payment_entry = tk.Entry(app)
down_payment_entry.pack()

interest_rate_label = tk.Label(app, text="Годовая процентная ставка (%):")
interest_rate_label.pack()
interest_rate_entry = tk.Entry(app)
interest_rate_entry.pack()

loan_term_label = tk.Label(app, text="Срок кредита (годы):")
loan_term_label.pack()
loan_term_entry = tk.Entry(app)
loan_term_entry.pack()

calculate_button = tk.Button(app, text="Рассчитать", command=calculate_payments)
calculate_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

payment_schedule_label = tk.Label(app, text="Схема платежей:")
payment_schedule_label.pack()
payment_schedule = tk.Text(app, height=10, width=40)
payment_schedule.pack()

app.mainloop()
