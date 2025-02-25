import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography - Hide Text in Image")
        self.root.geometry("500x400")

        tk.Label(root, text="Enter your secret message:").pack(pady=5)
        self.message_entry = tk.Entry(root, width=60)
        self.message_entry.pack(pady=5)

        tk.Label(root, text="Enter passcode:").pack(pady=5)
        self.passcode_entry = tk.Entry(root, width=60, show='*')
        self.passcode_entry.pack(pady=5)

        tk.Button(root, text="Select Image & Encode", command=self.encode_message).pack(pady=5)
        tk.Button(root, text="Select Image & Decode", command=self.decode_message).pack(pady=5)
        tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    def text_to_binary(self, text):
        return ''.join(format(ord(char), '08b') for char in text) + '1111111111111110'

    def binary_to_text(self, binary_str):
        chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        return ''.join(chr(int(char, 2)) for char in chars)

    def encode_message(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
        if not file_path:
            return

        img = Image.open(file_path)
        img = img.convert("RGB")
        img_array = np.array(img, dtype=np.uint8)
        message = self.message_entry.get()
        passcode = self.passcode_entry.get()

        if not message or not passcode:
            messagebox.showerror("Error", "Message and passcode cannot be empty!")
            return

        binary_message = self.text_to_binary(message) + '1111111111111110'

        data_index = 0

        for row in img_array:
            for pixel in row:
                for channel in range(3):
                    if data_index < len(binary_message):
                        passcode_value = ord(passcode[data_index % len(passcode)])
                        new_pixel_value = (int(pixel[channel]) + passcode_value) % 256
                        pixel[channel] = np.uint8((new_pixel_value & ~1) | int(binary_message[data_index]))
                        data_index += 1
                    else:
                        break

        output_path = "encryptedImage.png"
        encoded_img = Image.fromarray(img_array, "RGB")
        encoded_img.save(output_path)
        messagebox.showinfo("Success", "Message encoded successfully!")

    def decode_message(self):
        file_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("Image Files", ".png;.jpg;*.jpeg")])
        if not file_path:
            return

        img = Image.open(file_path)
        img = img.convert("RGB")
        img_array = np.array(img, dtype=np.uint8)

        passcode = self.passcode_entry.get()
        if not passcode:
            messagebox.showerror("Error", "Passcode cannot be empty!")
            return

        delimiter = '1111111111111110'
        binary_data = ''

        for row in img_array:
            for pixel in row:
                for channel in range(3):
                    binary_data += str(pixel[channel] & 1)

        if delimiter in binary_data:
            binary_message = binary_data.split(delimiter)[0]
            message = self.binary_to_text(binary_message[:-16])  # Remove the delimiter before decoding

        else:
            message = "No hidden message found."

        print(f"Hidden Message: {message}")
        messagebox.showinfo("Decoded Message", f"Hidden Message: {message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
