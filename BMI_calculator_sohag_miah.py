import time
import tkinter as tk
from tkinter import ttk, messagebox


class HealthMetricsApp:
    def __init__(self, window_root):
        self.root = window_root
        self.root.title("Body Mass Index Evaluator")
        self.root.geometry("620x420")
        self.root.configure(bg="#f4f4f9")

        self.setup_ui_styles()
        self.build_widgets()

    def setup_ui_styles(self):
        self.app_style = ttk.Style()
        self.app_style.configure('Custom.TButton', background='#2E7D32', font=('Segoe UI', 10, 'bold'))
        self.app_style.map('Custom.TButton', background=[('active', '#1B5E20')])

    def build_widgets(self):
        self.container = ttk.Frame(self.root, padding="25")
        self.container.pack(expand=True, fill="both")

        # Weight Input Section
        ttk.Label(self.container, text="Weight Input:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.input_weight = ttk.Entry(self.container, width=20)
        self.input_weight.grid(row=0, column=1, pady=5)

        self.unit_weight_var = tk.StringVar(value="kgs")
        self.selector_weight_unit = ttk.Combobox(
            self.container, 
            textvariable=self.unit_weight_var, 
            values=("kgs", "lbs"), 
            state="readonly", 
            width=7
        )
        self.selector_weight_unit.grid(row=0, column=2, padx=8, pady=5)

        # Height Input Section
        ttk.Label(self.container, text="Height Input:", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.input_height = ttk.Entry(self.container, width=20)
        self.input_height.grid(row=1, column=1, pady=5)

        self.unit_height_var = tk.StringVar(value="meters")
        self.selector_height_unit = ttk.Combobox(
            self.container, 
            textvariable=self.unit_height_var, 
            values=("meters", "feet"), 
            state="readonly", 
            width=7
        )
        self.selector_height_unit.grid(row=1, column=2, padx=8, pady=5)

        # Action Button
        self.btn_process = ttk.Button(
            self.container, 
            text="Calculate BMI", 
            command=self.process_health_data, 
            style='Custom.TButton'
        )
        self.btn_process.grid(row=2, column=0, columnspan=3, pady=15)

        # Output Display Labels
        self.disp_bmi = ttk.Label(self.container, text="BMI: --", font=("Segoe UI", 11))
        self.disp_bmi.grid(row=3, column=0, columnspan=3, sticky="w", pady=3)

        self.disp_category = ttk.Label(self.container, text="Category: --", font=("Segoe UI", 11))
        self.disp_category.grid(row=4, column=0, columnspan=3, sticky="w", pady=3)

        self.disp_ideal_weight = ttk.Label(self.container, text="Suggested Weight Range: --", font=("Segoe UI", 11))
        self.disp_ideal_weight.grid(row=5, column=0, columnspan=3, sticky="w", pady=3)

        self.disp_ideal_height = ttk.Label(self.container, text="Suggested Height Range: --", font=("Segoe UI", 11))
        self.disp_ideal_height.grid(row=6, column=0, columnspan=3, sticky="w", pady=3)

    # Core Calculations Logic
    @staticmethod
    def compute_bmi_value(weight_kg, height_m):
        return weight_kg / (height_m ** 2)

    @staticmethod
    def classify_bmi(bmi_val):
        if bmi_val < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_val < 25:
            return "Normal Weight"
        elif 25 <= bmi_val < 30:
            return "Overweight"
        else:
            return "Obese"

    @staticmethod
    def estimate_optimal_weight(height_m):
        min_wt = 18.5 * (height_m ** 2)
        max_wt = 24.9 * (height_m ** 2)
        return min_wt, max_wt

    @staticmethod
    def estimate_optimal_height(weight_kg):
        min_ht = (weight_kg / 24.9) ** 0.5
        max_ht = (weight_kg / 18.5) ** 0.5
        return min_ht, max_ht

    def apply_ui_flash(self, target_widget, color_sequence, duration=0.1, iterations=5):
        for _ in range(iterations):
            for property_name, property_val in color_sequence:
                target_widget.configure(**{property_name: property_val})
                self.root.update()
                time.sleep(duration)

    def process_health_data(self):
        try:
            raw_weight = float(self.input_weight.get())
            raw_height = float(self.input_height.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for height and weight.")
            return

        # Convert unit inputs to SI units (kg, meters)
        processed_weight = raw_weight * 0.453592 if self.unit_weight_var.get() == "lbs" else raw_weight
        processed_height = raw_height * 0.3048 if self.unit_height_var.get() == "feet" else raw_height

        if processed_height <= 0 or processed_weight <= 0:
            messagebox.showwarning("Input Range Error", "Values must be greater than zero.")
            return

        computed_bmi = self.compute_bmi_value(processed_weight, processed_height)
        health_status = self.classify_bmi(computed_bmi)

        opt_weight_low, opt_weight_high = self.estimate_optimal_weight(processed_height)
        opt_height_low, opt_height_high = self.estimate_optimal_height(processed_weight)

        # Update Text Values
        self.disp_bmi.config(text=f"BMI: {computed_bmi:.2f}")
        self.disp_category.config(text=f"Category: {health_status}")
        self.disp_ideal_weight.config(text=f"Suggested Weight Range: {opt_weight_low:.2f} - {opt_weight_high:.2f} kg")
        self.disp_ideal_height.config(text=f"Suggested Height Range: {opt_height_low:.2f} - {opt_height_high:.2f} meters")

        # Run Interface Animations
        self.apply_ui_flash(self.disp_bmi, [("background", "green"), ("background", "SystemButtonFace")])
        self.apply_ui_flash(self.disp_category, [("background", "yellow"), ("background", "SystemButtonFace")])
        self.apply_ui_flash(self.disp_ideal_weight, [("background", "orange"), ("background", "SystemButtonFace")])
        self.apply_ui_flash(self.disp_ideal_height, [("background", "red"), ("background", "SystemButtonFace")])


if __name__ == "__main__":
    app_root = tk.Tk()
    app_instance = HealthMetricsApp(app_root)
    app_root.mainloop()