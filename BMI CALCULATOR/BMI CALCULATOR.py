import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BMICalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("800x600")
        self.root.configure(bg='#000000')
        
        # Data file setup
        self.data_file = "user_data.json"
        self.load_data()
        
        # Current user
        self.current_user = tk.StringVar()
        
        # Configure styles first
        self.setup_styles()
        
        self.create_interface()
    
    def setup_styles(self):
        """Setup custom styles for dark theme"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Combobox style
        self.style.configure('Custom.TCombobox', 
                           fieldbackground='#333333',
                           background='#333333',
                           foreground='#FFFFFF',
                           bordercolor='#666666',
                           arrowcolor='#FFFFFF')
        
        # Configure Treeview style for dark theme
        self.style.configure('Dark.Treeview',
                           background='#2a2a2a',
                          foreground='#FFFFFF',
                           fieldbackground='#2a2a2a',
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Dark.Treeview.Heading',
                           background='#1a1a1a',
                           foreground='#00FF41',
                           relief='flat',
                           borderwidth=1)
        
        # Map for selection colors
        self.style.map('Dark.Treeview',
                      background=[('selected', '#4a4a4a')],
                      foreground=[('selected', '#FFFFFF')])
    
    def load_data(self):
        """Load user data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.user_data = json.load(f)
            except:
                self.user_data = {}
        else:
            self.user_data = {}
    
    def create_interface(self):
        """Create the black-themed GUI interface"""
        # Title
        title_label = tk.Label(self.root, text="  BMI Calculator", 
                              font=('Arial', 20, 'bold'), bg='#000000', fg='#FFFFFF')
        title_label.pack(pady=20)
        
        # User selection frame
        user_frame = tk.Frame(self.root, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        user_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(user_frame, text="Select User:", font=('Arial', 12, 'bold'), 
                bg='#1a1a1a', fg='#FFFFFF').pack(side=tk.LEFT, padx=10, pady=10)
        
        self.user_combo = ttk.Combobox(user_frame, textvariable=self.current_user, 
                                     style='Custom.TCombobox', width=15)
        self.user_combo['values'] = list(self.user_data.keys())
        self.user_combo.pack(side=tk.LEFT, padx=5, pady=10)
        
        tk.Button(user_frame, text="➕ New User", command=self.add_new_user,
                 bg='#333333', fg='#FFFFFF', font=('Arial', 10, 'bold'),
                 activebackground='#555555', bd=0, padx=10).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        input_frame.pack(pady=20, padx=20, fill=tk.X)
        
        tk.Label(input_frame, text="💪 Enter Your Measurements", font=('Arial', 14, 'bold'),
                bg='#1a1a1a', fg='#00FF41').pack(pady=10)
        
        # Weight and height inputs
        weight_frame = tk.Frame(input_frame, bg='#1a1a1a')
        weight_frame.pack(pady=10)
        
        tk.Label(weight_frame, text="Weight (kg):", font=('Arial', 12), 
                bg='#1a1a1a', fg='#FFFFFF').grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.weight_var = tk.StringVar()
        weight_entry = tk.Entry(weight_frame, textvariable=self.weight_var, 
                              font=('Arial', 12), width=15, bg='#333333', fg='#FFFFFF',
                              insertbackground='#FFFFFF', bd=2, relief=tk.FLAT)
        weight_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(weight_frame, text="Height (cm):", font=('Arial', 12), 
                bg='#1a1a1a', fg='#FFFFFF').grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.height_var = tk.StringVar()
        height_entry = tk.Entry(weight_frame, textvariable=self.height_var, 
                              font=('Arial', 12), width=15, bg='#333333', fg='#FFFFFF',
                              insertbackground='#FFFFFF', bd=2, relief=tk.FLAT)
        height_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Calculate button
        calc_button = tk.Button(self.root, text="🔥 Calculate BMI", command=self.calculate_bmi,
                               bg='#00FF41', fg='#000000', font=('Arial', 14, 'bold'), 
                               width=15, height=2, activebackground='#00CC33', bd=0)
        calc_button.pack(pady=20)
        
        # Result display
        self.result_frame = tk.Frame(self.root, bg='#000000')
        self.result_frame.pack(pady=10)
        
        # Action buttons
        button_frame = tk.Frame(self.root, bg='#000000')
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="📊 View History", command=self.show_history,
                 bg='#FF6B35', fg='#FFFFFF', font=('Arial', 12, 'bold'),
                 activebackground='#E55A2B', bd=0, padx=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="📈 Show Trends", command=self.show_trends,
                 bg='#9B5DE5', fg='#FFFFFF', font=('Arial', 12, 'bold'),
                 activebackground='#7B47C7', bd=0, padx=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="📋 Statistics", command=self.show_statistics_window,
                 bg='#F15BB5', fg='#FFFFFF', font=('Arial', 12, 'bold'),
                 activebackground='#D13A96', bd=0, padx=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="🗑️ Clear", command=self.clear_results,
                 bg='#FF3333', fg='#FFFFFF', font=('Arial', 12, 'bold'),
                 activebackground='#CC0000', bd=0, padx=10).pack(side=tk.LEFT, padx=5)
    
    def validate_input(self, weight, height):
        """Validate user inputs"""
        try:
            weight_val = float(weight)
            height_val = float(height)
            
            if weight_val <= 0 or weight_val > 500:
                raise ValueError("Weight must be between 1-500 kg")
            
            if height_val <= 0 or height_val > 300:
                raise ValueError("Height must be between 1-300 cm")
                
            return weight_val, height_val/100
            
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError("Please enter valid numbers")
            else:
                raise e
    
    def calculate_bmi_value(self, weight, height):
        """Calculate BMI using the standard formula"""
        return weight / (height ** 2)
    
    def get_bmi_category(self, bmi):
        """Categorize BMI value with dark theme colors"""
        if bmi < 18.5:
            return "Underweight", "#00BFFF"
        elif 18.5 <= bmi < 25:
            return "Normal", "#00FF41"
        elif 25 <= bmi < 30:
            return "Overweight", "#FFB74D"
        else:
            return "Obese", "#FF5252"
    
    def calculate_bmi(self):
        """Main BMI calculation function"""
        try:
            # Clear previous results
            for widget in self.result_frame.winfo_children():
                widget.destroy()
                
            # Validate inputs
            weight, height = self.validate_input(self.weight_var.get(), self.height_var.get())
            
            # Calculate BMI
            bmi = self.calculate_bmi_value(weight, height)
            category, color = self.get_bmi_category(bmi)
            
            # Create result display
            result_container = tk.Frame(self.result_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
            result_container.pack(pady=10, padx=20, fill=tk.X)
            
            tk.Label(result_container, text=f"Your BMI: {bmi:.1f}", 
                    font=('Arial', 24, 'bold'), bg='#1a1a1a', fg='#FFFFFF').pack(pady=10)
            
            tk.Label(result_container, text=f"Category: {category}", 
                    font=('Arial', 16, 'bold'), bg='#1a1a1a', fg=color).pack(pady=5)
            
            # Health tip
            self.show_health_tips(bmi, category, result_container)
            
            # Save data if user is selected
            if self.current_user.get():
                self.save_bmi_data(weight, height*100, bmi, category)
                messagebox.showinfo("✅ Success", "BMI calculated and saved successfully!")
            else:
                messagebox.showwarning("⚠️ No User", "Select or create a user to save data!")
                
        except ValueError as e:
            messagebox.showerror("❌ Invalid Input", str(e))
        except Exception as e:
            messagebox.showerror("❌ Error", f"An error occurred: {str(e)}")
    
    def show_health_tips(self, bmi, category, parent_frame):
        """Display health recommendations"""
        tips = {
            "Underweight": "💡 Consider consulting a healthcare provider for weight gain strategies.",
            "Normal": "🎉 Excellent! Maintain your current lifestyle with regular exercise and balanced diet.",
            "Overweight": "⚠️ Consider increasing physical activity and consulting a nutritionist.",
            "Obese": "🏥 Consult a healthcare provider for personalized weight management plan."
        }
        
        tip_text = tips.get(category, "Maintain a healthy lifestyle!")
        
        tip_frame = tk.Frame(parent_frame, bg='#2a2a2a', relief=tk.RIDGE, bd=1)
        tip_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(tip_frame, text=tip_text, font=('Arial', 11), 
                bg='#2a2a2a', fg='#CCCCCC', wraplength=400).pack(pady=10, padx=10)
    
    def add_new_user(self):
        """Add a new user"""
        user_window = tk.Toplevel(self.root)
        user_window.title("Add New User")
        user_window.geometry("350x200")
        user_window.configure(bg='#000000')
        
        tk.Label(user_window, text="👤 Enter Username:", font=('Arial', 14, 'bold'), 
                bg='#000000', fg='#FFFFFF').pack(pady=20)
        
        username_var = tk.StringVar()
        username_entry = tk.Entry(user_window, textvariable=username_var, 
                                font=('Arial', 12), bg='#333333', fg='#FFFFFF',
                                insertbackground='#FFFFFF', width=25, bd=2, relief=tk.FLAT)
        username_entry.pack(pady=10)
        
        def save_user():
            username = username_var.get().strip()
            if username:
                if username not in self.user_data:
                    self.user_data[username] = []
                    self.save_data()
                    self.user_combo['values'] = list(self.user_data.keys())
                    self.current_user.set(username)
                    user_window.destroy()
                    messagebox.showinfo("✅ Success", f"User '{username}' added successfully!")
                else:
                    messagebox.showerror("❌ Error", "Username already exists!")
            else:
                messagebox.showerror("❌ Error", "Please enter a username!")
        
        tk.Button(user_window, text="✅ Add User", command=save_user,
                 bg='#00FF41', fg='#000000', font=('Arial', 12, 'bold'),
                 activebackground='#00CC33', bd=0, padx=20).pack(pady=20)
        
        username_entry.focus()
    
    def save_bmi_data(self, weight, height, bmi, category):
        """Save BMI calculation to user data"""
        username = self.current_user.get()
        if username not in self.user_data:
            self.user_data[username] = []
        
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'weight': weight,
            'height': height,
            'bmi': round(bmi, 1),
            'category': category
        }
        
        self.user_data[username].append(entry)
        self.save_data()
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            messagebox.showerror("❌ Save Error", f"Could not save data: {str(e)}")
    
    def show_history(self):
        """Display user's BMI history with FIXED dark theme display"""
        username = self.current_user.get()
        if not username:
            messagebox.showwarning("⚠️ No User", "Please select a user first!")
            return
            
        if username not in self.user_data or not self.user_data[username]:
            messagebox.showinfo("ℹ️ No Data", "No BMI history found for this user!")
            return
        
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title(f"BMI History - {username}")
        history_window.geometry("800x500")
        history_window.configure(bg='#000000')
        
        # Title
        tk.Label(history_window, text=f"📊 BMI History for {username}", 
                font=('Arial', 16, 'bold'), bg='#000000', fg='#FFFFFF').pack(pady=10)
        
        # Create main frame for history content
        main_frame = tk.Frame(history_window, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # FIXED: Using Text widget instead of Treeview for better dark theme support
        history_text = tk.Text(main_frame, font=('Courier', 11), bg='#2a2a2a', fg='#FFFFFF',
                              insertbackground='#FFFFFF', selectbackground='#4a4a4a',
                              selectforeground='#FFFFFF', bd=0, wrap=tk.NONE)
        
        # Add scrollbars
        v_scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=history_text.yview)
        h_scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=history_text.xview)
        
        history_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Create header
        header = f"{'#':<3} {'Date & Time':<20} {'Weight (kg)':<12} {'Height (cm)':<12} {'BMI':<8} {'Category':<12}\n"
        header += "=" * 80 + "\n"
        
        history_text.insert(tk.END, header)
        
        # Add data rows with proper formatting
        for i, entry in enumerate(reversed(self.user_data[username]), 1):
            date_str = entry['date'][:16]  # Truncate seconds for display
            weight_str = f"{entry['weight']:.1f}"
            height_str = f"{entry['height']:.0f}"
            bmi_str = f"{entry['bmi']:.1f}"
            category_str = entry['category']
            
            row = f"{i:<3} {date_str:<20} {weight_str:<12} {height_str:<12} {bmi_str:<8} {category_str:<12}\n"
            history_text.insert(tk.END, row)
        
        # Make text widget read-only
        history_text.config(state=tk.DISABLED)
        
        # Pack everything
        history_text.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Add statistics at bottom
        self.show_statistics(history_window, username)
        
        # Add action buttons
        btn_frame = tk.Frame(history_window, bg='#000000')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="🗑️ Delete Selected Record", command=lambda: self.delete_record(username),
                 bg='#FF3333', fg='#FFFFFF', font=('Arial', 10), bd=0, padx=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="💾 Export History", command=lambda: self.export_history(username),
                 bg='#9B5DE5', fg='#FFFFFF', font=('Arial', 10), bd=0, padx=10).pack(side=tk.LEFT, padx=5)
    
    def show_statistics(self, parent_window, username):
        """Show BMI statistics"""
        data = self.user_data[username]
        if len(data) < 1:
            return
            
        bmis = [entry['bmi'] for entry in data]
        avg_bmi = sum(bmis) / len(bmis)
        min_bmi = min(bmis)
        max_bmi = max(bmis)
        
        stats_frame = tk.Frame(parent_window, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(stats_frame, 
                text=f"📈 Stats: Records: {len(data)} | Avg BMI: {avg_bmi:.1f} | Min: {min_bmi:.1f} | Max: {max_bmi:.1f}",
                font=('Arial', 12, 'bold'), bg='#1a1a1a', fg='#00FF41').pack(pady=10)
    
    def delete_record(self, username):
        """Delete the most recent record"""
        if username in self.user_data and self.user_data[username]:
            if messagebox.askyesno("Confirm Delete", "Delete the most recent BMI record?"):
                self.user_data[username].pop()  # Remove last record
                self.save_data()
                messagebox.showinfo("✅ Success", "Record deleted successfully!")
        else:
            messagebox.showwarning("⚠️ No Data", "No records to delete!")
    
    def export_history(self, username):
        """Export history to file"""
        if username not in self.user_data or not self.user_data[username]:
            messagebox.showwarning("⚠️ No Data", "No history to export!")
            return
        
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")],
                title="Export BMI History"
            )
            
            if filename:
                if filename.endswith('.json'):
                    with open(filename, 'w') as f:
                        json.dump({username: self.user_data[username]}, f, indent=2)
                else:
                    with open(filename, 'w') as f:
                        f.write(f"BMI History for {username}\n")
                        f.write("=" * 50 + "\n\n")
                        for i, entry in enumerate(self.user_data[username], 1):
                            f.write(f"Record #{i}\n")
                            f.write(f"Date: {entry['date']}\n")
                            f.write(f"Weight: {entry['weight']:.1f} kg\n")
                            f.write(f"Height: {entry['height']:.0f} cm\n")
                            f.write(f"BMI: {entry['bmi']:.1f}\n")
                            f.write(f"Category: {entry['category']}\n")
                            f.write("-" * 30 + "\n\n")
                
                messagebox.showinfo("✅ Success", f"History exported to {filename}")
        
        except Exception as e:
            messagebox.showerror("❌ Export Error", f"Could not export: {str(e)}")
    
    def show_trends(self):
        """Display BMI trends graph"""
        username = self.current_user.get()
        if not username or username not in self.user_data or len(self.user_data[username]) < 2:
            messagebox.showwarning("⚠️ Insufficient Data", "Need at least 2 BMI records to show trends!")
            return
        
        # Create graph window
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"BMI Trends - {username}")
        graph_window.geometry("800x600")
        graph_window.configure(bg='#000000')
        
        # Prepare data
        data = self.user_data[username]
        dates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') for entry in data]
        bmis = [entry['bmi'] for entry in data]
        
        # Create matplotlib figure with dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), facecolor='#000000')
        ax.set_facecolor('#1a1a1a')
        
        # Plot with bright colors
        ax.plot(dates, bmis, marker='o', linewidth=3, markersize=8, 
               color='#00FF41', markerfacecolor='#FFFFFF', markeredgecolor='#00FF41')
        
        # Add BMI category zones
        ax.axhspan(0, 18.5, alpha=0.2, color='#00BFFF', label='Underweight')
        ax.axhspan(18.5, 25, alpha=0.2, color='#00FF41', label='Normal')
        ax.axhspan(25, 30, alpha=0.2, color='#FFB74D', label='Overweight')
        ax.axhspan(30, 50, alpha=0.2, color='#FF5252', label='Obese')
        
        ax.set_title(f'📈 BMI Trends for {username}', fontsize=16, fontweight='bold', color='#FFFFFF')
        ax.set_xlabel('Date', fontsize=12, color='#FFFFFF')
        ax.set_ylabel('BMI', fontsize=12, color='#FFFFFF')
        ax.grid(True, alpha=0.3, color='#666666')
        ax.legend(facecolor='#2a2a2a', edgecolor='#666666', labelcolor='#FFFFFF')
        
        ax.tick_params(colors='#FFFFFF')
        plt.xticks(rotation=45, color='#FFFFFF')
        plt.yticks(color='#FFFFFF')
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_statistics_window(self):
        """Show detailed statistics window"""
        username = self.current_user.get()
        if not username:
            messagebox.showwarning("⚠️ No User", "Please select a user first!")
            return
            
        if username not in self.user_data or not self.user_data[username]:
            messagebox.showinfo("ℹ️ No Data", "No BMI history found for this user!")
            return
        
        stats_window = tk.Toplevel(self.root)
        stats_window.title(f"BMI Statistics - {username}")
        stats_window.geometry("500x400")
        stats_window.configure(bg='#000000')
        
        tk.Label(stats_window, text=f"📊 BMI Statistics for {username}", 
                font=('Arial', 16, 'bold'), bg='#000000', fg='#FFFFFF').pack(pady=20)
        
        # Calculate statistics
        data = self.user_data[username]
        bmis = [entry['bmi'] for entry in data]
        weights = [entry['weight'] for entry in data]
        
        avg_bmi = sum(bmis) / len(bmis)
        min_bmi = min(bmis)
        max_bmi = max(bmis)
        avg_weight = sum(weights) / len(weights)
        
        # Display statistics
        stats_frame = tk.Frame(stats_window, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        stats_info = [
            ("📋 Total Records", len(data)),
            ("📊 Average BMI", f"{avg_bmi:.1f}"),
            ("📉 Minimum BMI", f"{min_bmi:.1f}"),
            ("📈 Maximum BMI", f"{max_bmi:.1f}"),
            ("⚖️ Average Weight", f"{avg_weight:.1f} kg"),
            ("📏 BMI Range", f"{max_bmi - min_bmi:.1f}"),
        ]
        
        for i, (label, value) in enumerate(stats_info):
            row_frame = tk.Frame(stats_frame, bg='#1a1a1a')
            row_frame.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(row_frame, text=label, font=('Arial', 12, 'bold'), 
                    bg='#1a1a1a', fg='#00FF41', anchor='w').pack(side=tk.LEFT)
            tk.Label(row_frame, text=str(value), font=('Arial', 12), 
                    bg='#1a1a1a', fg='#FFFFFF', anchor='e').pack(side=tk.RIGHT)
    
    def clear_results(self):
        """Clear the results display"""
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        messagebox.showinfo("✅ Cleared", "Results cleared successfully!")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = BMICalculator()
    app.run()
