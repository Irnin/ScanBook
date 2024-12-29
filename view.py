import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class View(tk.Tk):
	def __init__(self, controller):
		super().__init__()
		self.controller = controller

		self.title('ScanBooks')

		# TKINTER VARIABLES
		self.tk_name = tk.StringVar()

		file_path = self.controller.get_files_path()
		self.tk_path = tk.StringVar(value=file_path)

		self.create_camera_view()
		self.create_treeview_view()
		self.create_input_view()

	def main(self):
		self.mainloop()

	def _open_settings_window(self):
		settings_window = tk.Toplevel(self)

		settings_window.title('Settings')


		path_label = tk.Label(settings_window, textvariable=self.tk_path)
		path_label.pack()

	def ask_for_path(self):
		my_dir = filedialog.askdirectory()
		self.controller.update_files_path(my_dir)

	def set_path(self, path):
		self.tk_path.set(path)

	# CAMERA VIEW
	def create_camera_view(self):
		self.camera_frame = tk.Frame()

		self.camera_view = tk.Label(self.camera_frame)
		self.camera_view.pack()

		self.camera_frame.pack(side='left', fill='both', padx=20, pady=20)
		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

	def load_frame(self, image_pil):
		self.camera_view.configure(image=image_pil)
		self.camera_view.image = image_pil

	def _save_image_action(self):
		filename = self.tk_name.get()
		self.controller.save_image_from_camera(filename)

	# TREE VIEW
	def create_treeview_view(self):
		self.treeview_frame = tk.Frame()

		# Path frame
		path_frame = tk.Frame(self.treeview_frame)
		path_frame.pack(pady=5)

		select_path_button = tk.Button(path_frame, text='Select directory', command=lambda: self.ask_for_path())
		select_path_button.pack(side='left')

		path_label = tk.Label(path_frame, textvariable=self.tk_path)
		path_label.pack(side='left', expand=True, fill='x')

		self.treeview = ttk.Treeview(self.treeview_frame, selectmode='browse')

		self.treeview.configure(columns='counter')
		self.treeview.heading('#0', text='File name')
		self.treeview.heading('counter', text='Counter')

		self.treeview.pack(fill='both', expand=True)

		self.treeview_frame.pack(side='left', fill='y', expand=True, padx=20, pady=20)
		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

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

	def clear_treeview(self):

		for children in self.treeview.get_children():
			self.treeview.delete(children)

	def create_input_view(self):
		input_frame = tk.Frame(self)

		name_entry = tk.Entry(input_frame, textvariable=self.tk_name)
		name_entry.pack()

		save_button = tk.Button(input_frame, text='Save', command=lambda: self._save_image_action())
		save_button.pack()
		self.bind('<Return>', lambda e: self._save_image_action())

		settings_button = tk.Button(input_frame, text='Settings', command=lambda: self._open_settings_window())
		settings_button.pack()

		input_frame.pack(side='left', padx=20, pady=20)