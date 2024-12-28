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

		# TREE VIEW
		self.treeview_frame = tk.Frame()
		self.treeview = ttk.Treeview(self.treeview_frame, selectmode='browse')

		self.treeview.configure(columns='counter')
		self.treeview.heading('#0', text='File name')
		self.treeview.heading('counter', text='Counter')

		self.treeview.pack(fill='both', expand=True)

		self.treeview_frame.pack(side='left', fill='y', expand=True, padx=20, pady=20)
		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

		# INPUT VIEW
		input_frame = tk.Frame(self)

		name_entry = tk.Entry(input_frame, textvariable=self.tk_name)
		name_entry.pack()

		save_button = tk.Button(input_frame, text='Save', command=lambda: self._save_image_action())
		save_button.pack()
		self.bind('<Return>', lambda e: self._save_image_action())

		input_frame.pack(side='left', padx=20, pady=20)

	def _save_image_action(self):
		filename = self.tk_name.get()
		self.controller.save_image_from_camera(filename)

	def load_frame(self, image_pil):
		self.camera_view.configure(image=image_pil)
		self.camera_view.image = image_pil

	def load_data_to_treeview(self, file_list):
		"""
		Loading data from file_list to treeview
		"""
		for key, list in file_list.items():
			key = self.treeview.insert(parent='', index=tk.END, text=key)

			list = sorted(list)

			for file in list:
				self.treeview.insert(parent=key, index=tk.END, values=file)

	def add_data_to_treeview(self, name, number):
		"""
		Method is adding file to treeview
		"""
		matched = False

		for child in self.treeview.get_children():
			element = list(self.treeview.item(child).values())
			if name == element[0]:
				self.treeview.insert(parent=child, index=tk.END, values=number)
				matched = True

		if not matched:
			row = self.treeview.insert(parent='', index=tk.END, text=name)
			self.treeview.insert(parent=row, index=tk.END, values=number)

	def main(self):
		self.mainloop()