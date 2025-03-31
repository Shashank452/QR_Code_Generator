import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import os
import webbrowser

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("600x600")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        style = ttk.Style()
        style.configure('Custom.TButton', padding=10, font=('Arial', 10))
        style.configure('Custom.TLabel', font=('Arial', 11))
        style.configure('Custom.TEntry', font=('Arial', 11))
        
        # Main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.input_frame, text="Enter Text or URL:", style='Custom.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.text_entry = ttk.Entry(self.input_frame, style='Custom.TEntry')
        self.text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Generate button
        self.generate_btn = ttk.Button(self.main_frame, text="Generate QR Code", 
                                      style='Custom.TButton', 
                                      command=self.generate_qr)
        self.generate_btn.pack(pady=10)
        
        # Save button
        self.save_btn = ttk.Button(self.main_frame, text="Save QR Code", 
                                  style='Custom.TButton', 
                                  command=self.save_qr)
        self.save_btn.pack(pady=10)
        
        # Preview section
        self.preview_frame = ttk.LabelFrame(self.main_frame, text="QR Code Preview")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.pack(pady=10)
        
        # Bind Enter key to generate
        self.root.bind('<Return>', lambda e: self.generate_qr())
        
        # Initialize QR code
        self.qr_code = None
        self.preview_image = None

    def generate_qr(self):
        try:
            data = self.text_entry.get()
            if not data:
                messagebox.showwarning("Input Required", "Please enter some text or URL")
                return
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            self.qr_code = qr.make_image(fill_color="black", back_color="white")
            
            # Update preview
            self.update_preview()
            
            self.status_label.configure(text="QR code generated successfully!", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def update_preview(self):
        if self.qr_code:
            # Convert to PhotoImage
            self.preview_image = ImageTk.PhotoImage(self.qr_code)
            self.preview_label.configure(image=self.preview_image)
            self.preview_label.image = self.preview_image

    def save_qr(self):
        if not self.qr_code:
            messagebox.showwarning("No QR Code", "Please generate a QR code first")
            return
            
        # Open file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            initialfile="qrcode.png"
        )
        
        if file_path:
            try:
                self.qr_code.save(file_path)
                self.status_label.configure(text=f"QR code saved to {os.path.basename(file_path)}", foreground="green")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()