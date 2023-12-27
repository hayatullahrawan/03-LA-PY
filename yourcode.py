from PIL import Image
import tkinter as tk
from tkinter import filedialog

def process_image(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = []
    
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            
            if r <1 and g <1 and b <1:
                neighbors = []
                for i in range(-20, 10):
                    for j in range(-20, 10):
                        if i == 0 and j ==0:
                            continue
                        if 0 <= x + i < width and 0 <= y + j < height:
                            nr, ng, nb = img.getpixel((x + i, y + j))
                            if nr >1 or ng >1 or nb >1:
                                neighbors.append((nr, ng, nb))
                if neighbors:
                    mean_r = sum(n[0] for n in neighbors) // len(neighbors)
                    mean_g = sum(n[1] for n in neighbors) // len(neighbors)
                    mean_b = sum(n[2] for n in neighbors) // len(neighbors)
                    r, g, b = mean_r, mean_g, mean_b
            row.append((r, g, b))
        pixels.append(row)
    
    new_img = Image.new("RGB", (width, height))
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[y][x]
            new_img.putpixel((x, y), (r, g, b))
    
    new_img.save("new_image.jpg")
    matrix = []
    
    for row in pixels:
        matrix_row = []
        for pixel in row:
            value = pixel[0] * 256 * 256 + pixel[1] * 256 + pixel[2]
            matrix_row.append(value)
        matrix.append(matrix_row)
    
    print(matrix)

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        process_image(file_path)

# Create the main window
window = tk.Tk()
window.title("Image Processing")
window.geometry("200x100")

# Create a button to browse for an image
browse_button = tk.Button(window, text="Browse", command=browse_image)
browse_button.pack(pady=20)

# Start the main event loop
window.mainloop()