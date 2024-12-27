import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ScanBooks')

		# TKINTER VARIABLES
		self.tk_name = tk.StringVar()

		# CAMERA VIEW
		self.camera_frame = tk.Frame()

		self.camera_view = tk.Label(self.camera_frame)
		self.camera_view.pack()

		self.camera_frame.pack(side='left', fill='both', padx=20, pady=20)

		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

		# INPUT VIEW
		input_frame = tk.Frame(self)

		name_entry = tk.Entry(input_frame, textvariable=self.tk_name)
		name_entry.pack()

		save_button = tk.Button(input_frame, text='Save', command=lambda: self.controller.save_image_from_camera(self.tk_name.get()))
		save_button.pack()

		input_frame.pack(side='left', padx=20, pady=20)

	def load_frame(self, image_pil):
		self.camera_view.configure(image=image_pil)
		self.camera_view.image = image_pil

	def main(self):
		self.mainloop()