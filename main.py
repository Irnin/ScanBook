import threading
import tkinter as tk
from PIL import Image, ImageTk
import cv2

image_counter = 0
file_name = ""
image = None
camera_view = None

class CameraThread(threading.Thread):
    def __init__(self, root, camera_view, camera_index=0):
        super().__init__()
        self.root = root
        self.camera_view = camera_view
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(self.camera_index)
        self.running = True  # Flag to stop the thread

    def run(self):
        while self.running:
            ret, frame = self.capture.read()

            if not ret:
                print("Failed to grab frame from camera.")
                break

            # Zmiana rozmiaru o 50% (zmniejszenie)
            scale_percent = 50  # Współczynnik skalowania w procentach
            width = int(frame.shape[1] * scale_percent / 100)  # Nowa szerokość
            height = int(frame.shape[0] * scale_percent / 100)  # Nowa wysokość
            dim = (width, height)

            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

            # Convert the OpenCV image to ImageTk format
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert colors
            image = Image.fromarray(image)  # Convert to PIL format
            image = ImageTk.PhotoImage(image)  # Convert to ImageTk format

            # Schedule the update of camera_view in the main thread
            self.root.after(0, self.update_image, image)

    def update_image(self, img):
        self.camera_view.configure(image=img)
        self.camera_view.image = img

    def stop(self):
        self.running = False
        self.capture.release()
        cv2.destroyAllWindows()

def save_image():
    global image_counter
    print("Saving image: {}_{}.png".format(file_name, image_counter))
    image_counter += 1

def save_image_thread():
	global counterEntryText
	counterEntryText.set(str(image_counter + 1))
	threading.Thread(target=save_image).start()

def bookEntryChanged(*args):
	global file_name
	file_name = bookEntryText.get()

# GUI
root = tk.Tk()
root.title("Book Scan By Kitku Soft")

# this will create a label widget
l1 = tk.Label(root, text="Book name")
l2 = tk.Label(root, text="Counter")

l1.grid(row=0, column=1, sticky=tk.W, pady=2)
l2.grid(row=1, column=1, sticky=tk.W, pady=2)

# entry widgets
bookEntryText = tk.StringVar()
bookEntryText.trace_add("write", bookEntryChanged)
bookNameEntry = tk.Entry(root, textvariable=bookEntryText)
bookNameEntry.grid(row=0, column=2, pady=2)

counterEntryText = tk.StringVar()
counterEntryText.set("{}".format(image_counter))
counterEntry = tk.Entry(root, textvariable=counterEntryText, state='readonly')
counterEntry.grid(row=1, column=2, pady=2)

# Image widget
default_image_path = "Image/noSignal.png"

image = Image.open(default_image_path).resize((400, 300))
image = ImageTk.PhotoImage(image)

camera_view = tk.Label(root, image=image)
camera_view.configure(image=image)
camera_view.image = image

camera_view.grid(row=0, column=0, rowspan = 5)


# Save Button
savePictureButton = tk.Button(root, text="Save picture", command=save_image_thread)
savePictureButton.grid(row=4, column=2, columnspan=2, pady=2)

# OpenCV
camera_thread = CameraThread(root, camera_view)
camera_thread.start()

tk.mainloop()

print("Closing the camera thread...")
camera_thread.stop()

