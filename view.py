import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
	def __init__(self, controller):
		super().__init__()

		self.title('ScanBooks')
		self.geometry('900x600')

		self.camera_frame = tk.Frame(bg='pink')

		self.camera_view = tk.Label(self.camera_frame)
		self.camera_view.pack()

		self.camera_frame.pack(fill='both')

		self.controller = controller

		tk.Button(text='Load image', command=lambda: self.controller.load_image()).pack()

	def load_frame(self, image_pil):
		self.camera_view.configure(image=image_pil)
		self.camera_view.image = image_pil

	def main(self):
		self.mainloop()