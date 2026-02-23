"""
Facebook Auto Registration - Final Fixed Version with Multiple Selectors
FOR EDUCATIONAL PURPOSES ONLY
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import string
from datetime import datetime
import os

# Auto ChromeDriver setup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class FinalFacebookBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Auto Registration - Final Version")
        self.root.geometry("1200x850")
        
        # Variables
        self.driver = None
        self.is_running = False
        self.phone_list = []
        self.current_index = 0
        self.wait = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main = ttk.Frame(self.root)
        main.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel
        left = ttk.LabelFrame(main, text="⚙️ Account Settings", padding=10)
        left.pack(side='left', fill='both', expand=True, padx=5)
        
        # Phone numbers
        ttk.Label(left, text="📱 Phone Numbers (এক লাইনে একটি নম্বর):", font=('Arial', 10, 'bold')).pack(anchor='w', pady=2)
        self.phone_text = scrolledtext.ScrolledText(left, height=8, width=35, font=('Consolas', 10))
        self.phone_text.pack(fill='x', pady=5)
        
        sample = """+84776108560
+84776108374
+84776104053
+84776106288
+84776103349"""
        self.phone_text.insert('1.0', sample)
        
        # Name settings
        ttk.Label(left, text="👤 First Names:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,2))
        self.first_names = tk.Text(left, height=3, width=35, font=('Consolas', 10))
        self.first_names.pack(fill='x')
        self.first_names.insert('1.0', "Rahul\nPriya\nAmit\nSneha\nRaj")
        
        ttk.Label(left, text="👤 Last Names:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10,2))
        self.last_names = tk.Text(left, height=3, width=35, font=('Consolas', 10))
        self.last_names.pack(fill='x')
        self.last_names.insert('1.0', "Kumar\nSingh\nSharma\nPatel\nDas")
        
        # DOB
        dob_frame = ttk.LabelFrame(left, text="🎂 Date of Birth Range", padding=5)
        dob_frame.pack(fill='x', pady=10)
        
        ttk.Label(dob_frame, text="Year:").grid(row=0, column=0, padx=2)
        self.dob_start = ttk.Entry(dob_frame, width=6)
        self.dob_start.insert(0, "1990")
        self.dob_start.grid(row=0, column=1)
        ttk.Label(dob_frame, text="-").grid(row=0, column=2)
        self.dob_end = ttk.Entry(dob_frame, width=6)
        self.dob_end.insert(0, "2000")
        self.dob_end.grid(row=0, column=3)
        
        # Options
        self.show_browser = tk.BooleanVar(value=True)
        ttk.Checkbutton(left, text="Show Browser (GUI Mode)", variable=self.show_browser).pack(anchor='w', pady=2)
        
        # Control buttons
        btn_frame = ttk.Frame(left)
        btn_frame.pack(fill='x', pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="▶ Start", command=self.start_bot, width=10)
        self.start_btn.pack(side='left', padx=2)
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹ Stop", command=self.stop_bot, state='disabled', width=10)
        self.stop_btn.pack(side='left', padx=2)
        
        self.debug_btn = ttk.Button(btn_frame, text="🔍 Debug Page", command=self.debug_page, width=12)
        self.debug_btn.pack(side='left', padx=2)
        
        # Progress
        self.progress = ttk.Progressbar(left, length=350, mode='determinate')
        self.progress.pack(fill='x', pady=5)
        
        # Status
        self.status_label = ttk.Label(left, text="✅ Ready", font=('Arial', 10))
        self.status_label.pack(pady=2)
        
        # Right panel - Logs
        right = ttk.LabelFrame(main, text="📋 Live Logs", padding=10)
        right.pack(side='right', fill='both', expand=True, padx=5)
        
        self.log_text = tk.Text(right, height=40, width=55, font=('Consolas', 9), bg='black', fg='lime')
        scrollbar = ttk.Scrollbar(right, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Configure tags
        self.log_text.tag_configure('info', foreground='cyan')
        self.log_text.tag_configure('success', foreground='lime')
        self.log_text.tag_configure('error', foreground='red')
        self.log_text.tag_configure('warning', foreground='yellow')
        self.log_text.tag_configure('debug', foreground='orange')
        
    def log(self, message, tag='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.root.update()
        
    def debug_page(self):
        """Debug current page structure"""
        if not self.driver:
            messagebox.showwarning("Warning", "No browser is running!")
            return
            
        try:
            self.log("🔍 Debugging page structure...", 'debug')
            
            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            self.log(f"Found {len(buttons)} buttons:", 'debug')
            for i, btn in enumerate(buttons):
                try:
                    text = btn.text
                    if text:
                        self.log(f"  Button {i+1}: '{text}'", 'debug')
                except:
                    pass
            
            # Find all submit inputs
            submits = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
            self.log(f"Found {len(submits)} submit inputs", 'debug')
            
            # Find all elements with name attribute
            elements = self.driver.find_elements(By.CSS_SELECTOR, "[name]")
            names = set()
            for elem in elements:
                try:
                    name = elem.get_attribute("name")
                    if name:
                        names.add(name)
                except:
                    pass
            self.log(f"Found name attributes: {', '.join(names)}", 'debug')
            
        except Exception as e:
            self.log(f"Debug error: {str(e)}", 'error')
        
    def start_bot(self):
        phones = [p.strip() for p in self.phone_text.get('1.0', tk.END).strip().split('\n') if p.strip()]
        
        if not phones:
            messagebox.showerror("Error", "কমপক্ষে একটি ফোন নম্বর দিন!")
            return
            
        self.phone_list = phones
        self.current_index = 0
        self.is_running = True
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.debug_btn.config(state='normal')
        
        self.progress['maximum'] = len(phones)
        self.progress['value'] = 0
        
        self.log("="*60, 'info')
        self.log(f"🚀 Starting bot with {len(phones)} phone numbers", 'info')
        self.log("="*60, 'info')
        
        self.root.after(1000, self.run_next_account)
        
    def stop_bot(self):
        self.is_running = False
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
                
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.debug_btn.config(state='disabled')
        self.log("⏹ Bot stopped", 'warning')
        
    def run_next_account(self):
        if not self.is_running:
            return
            
        if self.current_index >= len(self.phone_list):
            self.log("🎉 All accounts completed!", 'success')
            self.stop_bot()
            return
            
        phone = self.phone_list[self.current_index]
        self.current_index += 1
        
        self.progress['value'] = self.current_index
        
        thread = threading.Thread(target=self.create_account, args=(phone,))
        thread.daemon = True
        thread.start()
        
    def find_signup_button(self, driver):
        """Find signup button using multiple strategies"""
        button_selectors = [
            # Try different button texts
            (By.XPATH, "//button[contains(text(), 'Sign Up')]"),
            (By.XPATH, "//button[contains(text(), 'সাইন আপ')]"),
            (By.XPATH, "//button[contains(text(), 'Submit')]"),
            (By.XPATH, "//button[contains(text(), 'নিবন্ধন')]"),
            
            # Try by name (your original)
            (By.NAME, "websubmit"),
            
            # Try by type
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            
            # Try by class patterns (Facebook specific)
            (By.CSS_SELECTOR, "button._6j.mvm._6wk._6wl"),
            (By.CSS_SELECTOR, "button[aria-label*='Sign']"),
            
            # Try any button in the form
            (By.CSS_SELECTOR, "form button"),
            
            # Try by ID
            (By.ID, "u_0_s"),
            (By.ID, "u_0_t"),
            
            # Last resort - any visible button
            (By.XPATH, "//button[not(@disabled)]")
        ]
        
        for by, selector in button_selectors:
            try:
                button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((by, selector))
                )
                if button and button.is_displayed():
                    self.log(f"✅ Found button with: {by} = {selector}", 'success')
                    return button
            except:
                continue
                
        return None
        
    def create_account(self, phone):
        driver = None
        try:
            self.log(f"\n{'='*50}", 'info')
            self.log(f"📱 Account {self.current_index}/{len(self.phone_list)}: {phone}", 'info')
            
            # Setup Chrome
            options = Options()
            if self.show_browser.get():
                options.add_argument("--start-maximized")
            else:
                options.add_argument("--headless=new")
            
            # Anti-detection
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            self.log("🔄 Setting up ChromeDriver...", 'info')
            service = Service(ChromeDriverManager().install())
            
            self.log("🚀 Launching Chrome...", 'info')
            driver = webdriver.Chrome(service=service, options=options)
            self.driver = driver
            self.wait = WebDriverWait(driver, 10)
            
            # Go to Facebook
            driver.get("https://www.facebook.com/reg/")
            self.log("⏳ Waiting for page to load...", 'info')
            time.sleep(3)
            
            # Get random data
            first = random.choice(self.first_names.get('1.0', tk.END).strip().split())
            last = random.choice(self.last_names.get('1.0', tk.END).strip().split())
            day = str(random.randint(1, 28))
            month = str(random.randint(1, 12))
            year = str(random.randint(int(self.dob_start.get()), int(self.dob_end.get())))
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + "!@#"
            
            self.log(f"👤 Name: {first} {last}", 'success')
            
            # Fill form using JavaScript (most reliable)
            js_code = f"""
            // Helper function to set value
            function setValue(selector, value) {{
                var el = document.querySelector(selector);
                if(el) {{
                    el.value = value;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            }}
            
            // Try multiple selectors for each field
            setValue('input[name="firstname"]', '{first}');
            setValue('input[name="lastname"]', '{last}');
            setValue('input[name="reg_email__"]', '{phone}');
            setValue('input[name="reg_passwd__"]', '{password}');
            
            // Birthday
            var daySelect = document.querySelector('select[name="birthday_day"]');
            if(daySelect) daySelect.value = '{day}';
            
            var monthSelect = document.querySelector('select[name="birthday_month"]');
            if(monthSelect) monthSelect.value = '{month}';
            
            var yearSelect = document.querySelector('select[name="birthday_year"]');
            if(yearSelect) yearSelect.value = '{year}';
            
            // Gender Female
            var gender = document.querySelector('input[value="1"]');
            if(gender) gender.click();
            """
            
            driver.execute_script(js_code)
            time.sleep(2)
            
            # Find and click Sign Up button
            self.log("🔍 Looking for Sign Up button...", 'info')
            signup_button = self.find_signup_button(driver)
            
            if signup_button:
                # Scroll to button
                driver.execute_script("arguments[0].scrollIntoView(true);", signup_button)
                time.sleep(1)
                
                # Click using JavaScript (most reliable)
                driver.execute_script("arguments[0].click();", signup_button)
                self.log("✅ Sign Up button clicked!", 'success')
            else:
                self.log("⚠️ Could not find Sign Up button", 'warning')
                # Try JavaScript click on any submit button
                driver.execute_script("""
                    var forms = document.getElementsByTagName('form');
                    if(forms.length > 0) {
                        forms[0].submit();
                    }
                """)
                self.log("✅ Form submitted via JavaScript", 'success')
            
            time.sleep(5)
            
            # Check result
            current_url = driver.current_url
            if "checkpoint" in current_url or "confirm" in current_url:
                self.log("✅ Verification page loaded - OTP required", 'success')
            else:
                self.log("✅ Registration attempted", 'success')
            
            time.sleep(3)
            driver.quit()
            self.driver = None
            
            self.log(f"✅ Account {self.current_index} completed", 'success')
            
            if self.is_running:
                self.root.after(2000, self.run_next_account)
                
        except Exception as e:
            self.log(f"❌ Error: {str(e)}", 'error')
            if driver:
                driver.quit()
            if self.is_running:
                self.root.after(3000, self.run_next_account)

def main():
    # Install required packages if needed
    import subprocess
    import sys
    
    required = ['selenium', 'webdriver-manager']
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    root = tk.Tk()
    app = FinalFacebookBot(root)
    root.mainloop()

if __name__ == "__main__":
    main()