import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import re

def select_image(position):
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = img.resize(sizes[position])
        images[position] = img
        preview_img = img.resize((100, 100))  # Resize the preview image to 100x100 pixels
        img_tk = ImageTk.PhotoImage(preview_img)
        labels[position].config(image=img_tk)
        labels[position].image = img_tk

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder.set(folder_selected)

def get_next_filename(folder):
    files = os.listdir(folder)
    numbers = [int(re.findall(r'\d+', f)[0]) for f in files if re.findall(r'\d+', f)]
    next_number = max(numbers) + 1 if numbers else 1
    return os.path.join(folder, f'{next_number}.png')

def create_final_image():
    if not output_folder.get():
        print("Please select an output folder.")
        return
    background = Image.open('posters.png')
    for position, img in images.items():
        background.paste(img, positions[position])
    output_path = get_next_filename(output_folder.get())
    background.save(output_path)
    print(f"Final image saved as '{output_path}'")

# Define the positions where the images will be placed
positions = [(0, 0), (346, 0), (733, 58), (322, 620), (632, 320)]
sizes = [(341, 455), (285, 380), (182, 243), (273, 364), (372, 496)]
images = {}

# Create the main window
root = tk.Tk()
root.title("FunPosterMaker")
root.geometry("850x650")  # Set the window size
root.resizable(True, True)  # Make the window size constant

# Create a StringVar to store the output folder path
output_folder = tk.StringVar()

# Create a frame for the image selection buttons and labels
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

# Load and resize the predetermined image
image_path = 'posters.png'  # Replace with the path to your image file
image = Image.open(image_path)
image = image.resize((512, 512))  # Resize the image
image_tk = ImageTk.PhotoImage(image)
# Create a label to display the image
image_label = tk.Label(root, image=image_tk)
# Place the label at specific coordinates (e.g., x=100, y=50)
image_label.place(x=300, y=50)

# Create buttons and labels for each position with hard-coded positions and sizes
labels = {}
button_positions = [(10, 10), (10, 120), (10, 230), (10, 340), (10, 450)]
label_positions = [(150, 10), (150, 120), (150, 230), (150, 340), (150, 450)]
for i, position in enumerate(positions):
    btn = tk.Button(frame, text=f"Select Image {i+1}", command=lambda i=i: select_image(i))
    btn.place(x=button_positions[i][0], y=button_positions[i][1], width=120, height=30)
    lbl = tk.Label(frame)
    lbl.place(x=label_positions[i][0], y=label_positions[i][1], width=100, height=100)
    labels[i] = lbl

# Create a button to select the output folder
folder_btn = tk.Button(frame, text="Select Output Folder", command=select_output_folder)
folder_btn.place(x=10, y=560, width=120, height=30)

# Create a label to display the selected output folder
folder_lbl = tk.Label(frame, textvariable=output_folder)
folder_lbl.place(x=150, y=560, width=400, height=30)

# Create a button to generate the final image
final_btn = tk.Button(frame, text="Create Final Image", command=create_final_image)
final_btn.place(x=10, y=600, width=540, height=30)



# Run the GUI event loop
root.mainloop()