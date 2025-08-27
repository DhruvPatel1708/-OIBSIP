import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import math
import json
from datetime import datetime

class JSStylePasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("600x750")
        self.root.minsize(550, 600)
        # Modern turquoise gradient background
        self.root.configure(bg='#4ECDC4')  # Turquoise like in your image
        
        # Character sets (JavaScript style)
        self.chars = {
            'lowercase': "abcdefghijklmnopqrstuvwxyz",
            'uppercase': "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 
            'numbers': "0123456789",
            'symbols': "!@#$%^&*()-_=+[]{}|;:,.<>?"
        }
        
        # Password history
        self.password_history = []
        
        self.create_interface()
    
    def create_interface(self):
        """Create the modern turquoise-themed interface"""
        # Create main container
        main_container = tk.Frame(self.root, bg='#4ECDC4')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title (matching the image style)
        title_frame = tk.Frame(main_container, bg='#4ECDC4', height=80)
        title_frame.pack(fill=tk.X, pady=(20, 10))
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="Password Generator", 
                font=('Arial', 28, 'bold'), bg='#4ECDC4', fg='#2C5F41').pack(expand=True)  # Dark green text
        
        # Main content card (white background like in image)
        content_card = tk.Frame(main_container, bg='#FFFFFF', relief=tk.RAISED, bd=0)
        content_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Generated password display (at top like in image)
        password_display_frame = tk.Frame(content_card, bg='#F8F9FA', relief=tk.RAISED, bd=1)
        password_display_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.password_text = tk.Text(password_display_frame, height=2, font=('Courier', 14, 'bold'), 
                                   wrap=tk.WORD, bg='#F8F9FA', fg='#2C5F41', bd=0, 
                                   highlightthickness=0)
        self.password_text.pack(fill=tk.X, padx=15, pady=15)
        
        # Copy button (inline like in image)
        copy_btn = tk.Button(password_display_frame, text="📋", command=self.copy_password,
                           bg='#4ECDC4', fg='white', font=('Arial', 12), bd=0,
                           width=3, height=1)
        copy_btn.place(relx=0.95, rely=0.5, anchor=tk.E)
        
        # Settings card (gray background like in image)
        settings_card = tk.Frame(content_card, bg='#E8EAF0', relief=tk.RAISED, bd=1)
        settings_card.pack(fill=tk.X, padx=20, pady=10)
        
        # Password length section (matching image layout)
        length_frame = tk.Frame(settings_card, bg='#E8EAF0')
        length_frame.pack(fill=tk.X, padx=20, pady=15)
        
        length_label_frame = tk.Frame(length_frame, bg='#E8EAF0')
        length_label_frame.pack(fill=tk.X)
        
        tk.Label(length_label_frame, text="Password Length", font=('Arial', 14, 'bold'), 
                bg='#E8EAF0', fg='#2C5F41').pack(side=tk.LEFT)
        
        # Length value display (like in image)
        self.length_var = tk.IntVar(value=24)
        length_value_label = tk.Label(length_label_frame, text="24", font=('Arial', 14, 'bold'),
                                    bg='#4ECDC4', fg='white', width=4, height=1)
        length_value_label.pack(side=tk.RIGHT)
        
        # Length slider (modern style)
        self.length_scale = tk.Scale(length_frame, from_=6, to=50, 
                                   orient=tk.HORIZONTAL, variable=self.length_var,
                                   bg='#E8EAF0', fg='#2C5F41', highlightthickness=0,
                                   length=300, sliderlength=20, bd=0,
                                   troughcolor='#4ECDC4', activebackground='#45B7B8')
        self.length_scale.pack(fill=tk.X, pady=10)
        
        # Update length value display when slider changes
        def update_length_display(*args):
            length_value_label.config(text=str(self.length_var.get()))
        self.length_var.trace('w', update_length_display)
        
        # Character sets section (matching image checkboxes)
        self.include_upper = tk.BooleanVar(value=False)  # Unchecked like in image
        self.include_lower = tk.BooleanVar(value=False)  # Unchecked like in image
        self.include_nums = tk.BooleanVar(value=True)    # Checked like in image
        self.include_special = tk.BooleanVar(value=True) # Checked like in image
        
        charset_options = [
            (self.include_upper, 'Include Uppercase'),
            (self.include_lower, 'Include Lowercase'),
            (self.include_nums, 'Include Numbers'),
            (self.include_special, 'Include Symbols')
        ]
        
        for var, text in charset_options:
            option_frame = tk.Frame(settings_card, bg='#E8EAF0')
            option_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(option_frame, text=text, font=('Arial', 12), 
                    bg='#E8EAF0', fg='#2C5F41').pack(side=tk.LEFT)
            
            # Custom checkbox style (modern square)
            checkbox = tk.Checkbutton(option_frame, variable=var, bg='#E8EAF0', 
                                    selectcolor='#4ECDC4', bd=0, highlightthickness=0,
                                    activebackground='#E8EAF0')
            checkbox.pack(side=tk.RIGHT)
        
        # Generate button (matching image style)
        generate_btn = tk.Button(content_card, text="🔑 Generate Password", 
                               command=self.generate_password, bg='#4ECDC4', fg='white',
                               font=('Arial', 16, 'bold'), height=2, bd=0,
                               activebackground='#45B7B8')
        generate_btn.pack(fill=tk.X, padx=20, pady=20)
        
        # Password strength section (like in image)
        strength_frame = tk.Frame(content_card, bg='#FFFFFF')
        strength_frame.pack(fill=tk.X, padx=20, pady=10)
        
        strength_label_frame = tk.Frame(strength_frame, bg='#FFFFFF')
        strength_label_frame.pack(fill=tk.X)
        
        tk.Label(strength_label_frame, text="Password Strength:", font=('Arial', 12, 'bold'), 
                bg='#FFFFFF', fg='#2C5F41').pack(side=tk.LEFT)
        
        self.strength_var = tk.StringVar(value="Strong")
        self.strength_label = tk.Label(strength_label_frame, textvariable=self.strength_var, 
                                     font=('Arial', 12, 'bold'), bg='#FFFFFF', fg='#4ECDC4')
        self.strength_label.pack(side=tk.RIGHT)
        
        # Strength bar (like in image)
        strength_bar_frame = tk.Frame(strength_frame, bg='#FFFFFF', height=10)
        strength_bar_frame.pack(fill=tk.X, pady=5)
        
        self.strength_bar = tk.Frame(strength_bar_frame, bg='#4ECDC4', height=8)
        self.strength_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Footer buttons (minimal style)
        footer_frame = tk.Frame(main_container, bg='#4ECDC4', height=60)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        footer_frame.pack_propagate(False)
        
        button_container = tk.Frame(footer_frame, bg='#4ECDC4')
        button_container.pack(expand=True)
        
        # Minimal footer buttons
        tk.Button(button_container, text="History", command=self.show_history,
                 bg='#45B7B8', fg='white', font=('Arial', 10), bd=0, padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_container, text="Save", command=self.save_to_file,
                 bg='#45B7B8', fg='white', font=('Arial', 10), bd=0, padx=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_container, text="Reset", command=self.reset_form,
                 bg='#45B7B8', fg='white', font=('Arial', 10), bd=0, padx=15).pack(side=tk.LEFT, padx=5)
    
    def generate_password(self):
        """JavaScript-style password generation function"""
        try:
            length = int(self.length_var.get())
            include_upper = self.include_upper.get()
            include_lower = self.include_lower.get() 
            include_nums = self.include_nums.get()
            include_special = self.include_special.get()
            
            if not (length >= 6 and length <= 50):
                messagebox.showerror("Invalid Length", "Password length must be between 6 and 50 characters!")
                return
            
            available_chars = ""
            
            if include_lower:
                available_chars += self.chars['lowercase']
            if include_upper:
                available_chars += self.chars['uppercase']
            if include_nums:
                available_chars += self.chars['numbers']
            if include_special:
                available_chars += self.chars['symbols']
            
            if not available_chars:
                messagebox.showerror("No Character Set", "Please select at least one character type!")
                return
            
            password = self.gen_pass(length, available_chars, include_upper, include_lower, include_nums, include_special)
            
            # Display password
            self.password_text.delete(1.0, tk.END)
            self.password_text.insert(1.0, password)
            
            # Calculate and show strength
            strength, color = self.check_password_strength(password)
            self.strength_var.set(strength)
            self.strength_label.config(fg=color)
            
            # Update strength bar
            self.update_strength_bar(strength)
            
            self.add_to_history(password, strength)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for length!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_strength_bar(self, strength):
        """Update the visual strength bar"""
        colors = {
            "Very Weak": "#FF4757",
            "Weak": "#FF6B7A", 
            "Good": "#FFA502",
            "Strong": "#4ECDC4",
            "Very Strong": "#2ED573"
        }
        
        widths = {
            "Very Weak": 0.2,
            "Weak": 0.4,
            "Good": 0.6, 
            "Strong": 0.8,
            "Very Strong": 1.0
        }
        
        color = colors.get(strength, "#4ECDC4")
        self.strength_bar.config(bg=color)
    
    def gen_pass(self, length, available_chars, upper, lower, nums, special):
        """JavaScript-style password generation"""
        password = ""
        mandatory_chars = ""
        
        if upper and self.chars['uppercase']:
            rand_upper = self.chars['uppercase'][math.floor(random.random() * len(self.chars['uppercase']))]
            mandatory_chars += rand_upper
        
        if lower and self.chars['lowercase']:
            rand_lower = self.chars['lowercase'][math.floor(random.random() * len(self.chars['lowercase']))]
            mandatory_chars += rand_lower
        
        if nums and self.chars['numbers']:
            rand_num = self.chars['numbers'][math.floor(random.random() * len(self.chars['numbers']))]
            mandatory_chars += rand_num
        
        if special and self.chars['symbols']:
            rand_special = self.chars['symbols'][math.floor(random.random() * len(self.chars['symbols']))]
            mandatory_chars += rand_special
        
        remaining_length = length - len(mandatory_chars)
        
        for i in range(remaining_length):
            rand_index = math.floor(random.random() * len(available_chars))
            password += available_chars[rand_index]
        
        password += mandatory_chars
        
        password_array = list(password)
        for i in range(len(password_array)):
            rand_index = math.floor(random.random() * len(password_array))
            password_array[i], password_array[rand_index] = password_array[rand_index], password_array[i]
        
        return ''.join(password_array)
    
    def check_password_strength(self, password):
        """JavaScript-style password strength checker"""
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        
        has_lower = any(c in self.chars['lowercase'] for c in password)
        has_upper = any(c in self.chars['uppercase'] for c in password)
        has_nums = any(c in self.chars['numbers'] for c in password)
        has_special = any(c in self.chars['symbols'] for c in password)
        
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_nums:
            score += 1
        if has_special:
            score += 1
        
        if score <= 2:
            return "Very Weak", "#FF4757"
        elif score <= 4:
            return "Weak", "#FF6B7A"
        elif score <= 5:
            return "Good", "#FFA502"
        elif score <= 6:
            return "Strong", "#4ECDC4"
        else:
            return "Very Strong", "#2ED573"
    
    def copy_password(self):
        """Copy password to clipboard"""
        password = self.password_text.get(1.0, tk.END).strip()
        if password:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(password)
                self.root.update()
                messagebox.showinfo("Copied", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Clipboard Error", f"Could not copy: {str(e)}")
        else:
            messagebox.showwarning("No Password", "Generate a password first!")
    
    def add_to_history(self, password, strength):
        """Add password to history"""
        entry = {
            'password': password,
            'strength': strength,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'length': len(password)
        }
        
        self.password_history.insert(0, entry)
        
        if len(self.password_history) > 10:
            self.password_history = self.password_history[:10]
    
    def show_history(self):
        """Display password history"""
        if len(self.password_history) == 0:
            messagebox.showinfo("No History", "No passwords generated yet.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")
        history_window.geometry("700x400")
        history_window.configure(bg='#4ECDC4')
        
        tk.Label(history_window, text="Password History", 
                font=('Arial', 16, 'bold'), bg='#4ECDC4', fg='#2C5F41').pack(pady=10)
        
        history_frame = tk.Frame(history_window, bg='#FFFFFF')
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        history_text = tk.Text(history_frame, font=('Courier', 10), bg='#FFFFFF', fg='#2C5F41')
        scrollbar = tk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_text.yview)
        history_text.configure(yscrollcommand=scrollbar.set)
        
        for i, entry in enumerate(self.password_history):
            history_text.insert(tk.END, f"#{i+1} - {entry['timestamp']}\n")
            history_text.insert(tk.END, f"Password: {entry['password']}\n")
            history_text.insert(tk.END, f"Length: {entry['length']} | Strength: {entry['strength']}\n")
            history_text.insert(tk.END, "-" * 50 + "\n\n")
        
        history_text.config(state=tk.DISABLED)
        
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def save_to_file(self):
        """Save password to file"""
        password = self.password_text.get(1.0, tk.END).strip()
        if not password:
            messagebox.showwarning("No Password", "Generate a password first!")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")],
                title="Save Password"
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(f"Generated Password: {password}\n")
                    f.write(f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Length: {len(password)}\n")
                    f.write(f"Strength: {self.strength_var.get()}\n")
                
                messagebox.showinfo("Saved", f"Password saved to {filename}")
        
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
    
    def reset_form(self):
        """Reset form to default values"""
        self.length_var.set(24)
        self.include_upper.set(False)
        self.include_lower.set(False) 
        self.include_nums.set(True)
        self.include_special.set(True)
        
        self.password_text.delete(1.0, tk.END)
        self.strength_var.set("Strong")
        self.strength_label.config(fg='#4ECDC4')
        self.strength_bar.config(bg='#4ECDC4')
        
        messagebox.showinfo("Reset", "Form reset to default values!")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = JSStylePasswordGenerator()
    app.run()
