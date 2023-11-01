import tkinter as tk

class CreditPaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Платежи по кредиту")
        
        # Переменные для хранения ввода пользователя
        self.principal_var = tk.DoubleVar()
        self.down_payment_var = tk.DoubleVar()
        self.interest_rate_var = tk.DoubleVar()
        self.loan_term_var = tk.IntVar()
        self.additional_payment_var = tk.DoubleVar()
        
        # Создание элементов интерфейса
        tk.Label(root, text="Цена покупки:").pack()
        self.principal_entry = tk.Entry(root, textvariable=self.principal_var)
        self.principal_entry.pack()
        
        tk.Label(root, text="Первоначальный платеж:").pack()
        self.down_payment_entry = tk.Entry(root, textvariable=self.down_payment_var)
        self.down_payment_entry.pack()
        
        tk.Label(root, text="Годовая процентная ставка (%):").pack()
        self.interest_rate_entry = tk.Entry(root, textvariable=self.interest_rate_var)
        self.interest_rate_entry.pack()
        
        tk.Label(root, text="Срок кредита (годы):").pack()
        self.loan_term_entry = tk.Entry(root, textvariable=self.loan_term_var)
        self.loan_term_entry.pack()
        
        tk.Label(root, text="Дополнительные платежи:").pack()
        self.additional_payment_entry = tk.Entry(root, textvariable=self.additional_payment_var)
        self.additional_payment_entry.pack()
        
        self.calculate_button = tk.Button(root, text="Рассчитать", command=self.calculate_payments)
        self.calculate_button.pack()
        
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
        self.payment_schedule_label = tk.Label(root, text="Схема платежей:")
        self.payment_schedule_label.pack()
        
        self.payment_schedule = tk.Text(root, height=10, width=40)
        self.payment_schedule.pack()
        
    def calculate_payments(self):
        principal = self.principal_var.get()
        down_payment = self.down_payment_var.get()
        interest_rate = self.interest_rate_var.get() / 100
        loan_term = self.loan_term_var.get()
        additional_payment = self.additional_payment_var.get()
        
        loan_amount = principal - down_payment
        monthly_interest_rate = interest_rate / 12
        num_payments = loan_term * 12
        monthly_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
        
        result_text = f"Ежемесячный платеж: {monthly_payment:.2f}"
        self.result_label.config(text=result_text)
        
        payment_schedule_text = ""
        balance = loan_amount
        total_principal_payments = 0
        total_interest_payments = 0
        
        for month in range(1, num_payments + 1):
            interest_payment = balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment - additional_payment
            balance -= principal_payment
            
            total_principal_payments += principal_payment
            total_interest_payments += interest_payment
            
            payment_schedule_text += f"Месяц {month}: Основной платеж: {principal_payment:.2f}, Платеж по процентам: {interest_payment:.2f}, Остаток долга: {balance:.2f}\n"
        
        self.payment_schedule.delete(1.0, tk.END)
        self.payment_schedule.insert(tk.END, payment_schedule_text)
        
        result_text += f"\nСумма всех основных платежей: {total_principal_payments:.2f}"
        result_text += f"\nСумма платежей по процентам (размер переплаты): {total_interest_payments:.2f}"
        
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CreditPaymentApp(root)
    root.mainloop()
