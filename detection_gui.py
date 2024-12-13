import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from utils.object_detector import detect_objects
from utils.file_handler import save_image
import cv2


class RetailDetectionApp:
    def __init__(self):
        self.detected_image_tk = None
        self.root = tk.Tk()
        self.root.title("Retail Object Detection")

        # Image display

        self.image_label = tk.Label(self.root, text="Upload an image for detection", font=("Helvetica", 12))
        self.image_label.pack(pady=10)
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)

        # Button
        tk.Button(self.root, text="Upload Image", command=self.upload_image).pack(pady=5)
        tk.Button(self.root, text="Detect Object", command=self.detect_objects).pack(pady=5)
        tk.Button(self.root, text="Save Result", command=self.save_result).pack(pady=5)

        self.image_path = None
        self.detected_image = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files :", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)
            image.thumbnail((600, 400))
            self.image= ImageTk.PhotoImage(image)
            self.canvas.create_image(300, 200, image=self.image)

    def detect_objects(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image uploaded.")
            return
        self.detected_image = detect_objects(self.image_path)
        detected_image_pil = Image.fromarray(cv2.cvtColor(self.detected_image, cv2.COLOR_BGRA2BGR))
        detected_image_pil.thumbnail((600, 400))
        self.detected_image_tk = ImageTk.PhotoImage(detected_image_pil)
        self.canvas.create_image(300, 200, image=self.detected_image_tk)

    def save_result(self):
        if self.detected_image is None:
            messagebox.showerror("Error", "No detection performed.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image Files", "*.jpg")])
        if output_path:
            save_image(self.detected_image, output_path)
            messagebox.showinfo("Success", "Result saved successfully.")

    def run(self):
        self.root.mainloop()
