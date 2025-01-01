import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from ScrollableFrame import ScrollableFrame

class View(tk.Tk):
	def __init__(self, controller, subjects: [str]):
		super().__init__()
		self.controller = controller
		self.subjects = subjects

		self.title('ScanBooks')
		self.resizable(False, False)

		# TKINTER VARIABLES
		self.tk_book_name = tk.StringVar()

		file_path = self.controller.get_files_path()
		self.tk_path = tk.StringVar(value=file_path)

		self.tk_selected_subject = tk.StringVar(value=self.subjects[0] if self.subjects else '')

		# FONT
		self.bold_font = ('Receiptional Receipt', 20, 'bold')

		# Creating interface
		self.create_camera_view()
		self.create_treeview_view()
		self.create_preview_view()

		self.bind('<Return>', lambda e: self._save_image_action())

	def load_subjects(self, subjects):
		self.subjects = []

		for subject in subjects:
			self.subjects.append(subject)

	def main(self):
		self.mainloop()

	def _open_settings_window(self):
		"""
		Method is opening settings window
		"""

		tk_new_subject = tk.StringVar()

		settings_window = tk.Toplevel(self)

		input_frame = tk.Frame(settings_window)
		input_frame.pack(fill='x', padx=10, pady=10)

		entry = tk.Entry(input_frame, textvariable=tk_new_subject)
		entry.pack(side='left', fill='x', expand=True)

		add_subject_button = tk.Button(input_frame, text='Add', command=lambda: _add_subject())
		add_subject_button.pack(side='right')

		self.subjects_settings_frame = ScrollableFrame(settings_window)
		self.subjects_settings_frame.pack(fill='both', expand=True, padx=10, pady=10)

		self.load_subjects_to_settings_view()

		settings_window.bind('<Return>', lambda e: _add_subject())

		def _add_subject():
			subject = tk_new_subject.get()
			self.controller.add_subject(subject)
			tk_new_subject.set('')

	def load_subjects_to_settings_view(self):
		self.subjects_settings_frame.clear_frame()

		for subject in self.subjects:
			frame = ttk.Frame(self.subjects_settings_frame.scrollable_frame)

			label = tk.Label(frame, text=subject)
			label.pack(side='left', anchor='w')

			remove_subject_button = tk.Button(frame, text='Remove', command=lambda s=subject: self.controller.remove_subject(s))
			remove_subject_button.pack(side='right')

			frame.pack(expand=True, fill='x')
			separator = ttk.Separator(self.subjects_settings_frame.scrollable_frame, orient='horizontal')
			separator.pack(fill='x')

	def load_subjects_to_input_view(self):
		menu = self.subject_menu['menu']
		menu.delete(0, 'end')

		for subject in self.subjects:
			menu.add_command(label=subject, command=lambda s = subject: self.tk_selected_subject.set(s))

		selected_subject = self.tk_selected_subject.get()

		if not selected_subject in self.subjects:
			selected_subject = self.subjects[0] if self.subjects else 'WithoutSubject'
			self.tk_selected_subject.set(selected_subject)

	def ask_for_path(self):
		"""
		Method is opening window to provide directory to work with and update settings
		"""

		my_dir = filedialog.askdirectory()
		self.controller.update_files_path(my_dir)

	def set_path(self, path):
		"""
		Update tkinter path variable with provided string
		"""

		self.tk_path.set(path)

	# CAMERA VIEW
	def create_camera_view(self):
		"""
		Creating camera view
		"""

		camera_frame = tk.Frame()
		camera_frame.pack(side='left', fill='both', padx=20, pady=20)

		tk.Label(camera_frame, text='Camera:', font=self.bold_font).pack(anchor='w')

		self.camera_view = tk.Label(camera_frame)
		self.camera_view.pack()

		ttk.Separator(camera_frame, orient='horizontal').pack(fill='x', pady=10)

		input_box = tk.Frame(camera_frame)
		input_box.pack(fill='x')

		input_box.rowconfigure((0, 1), weight=1)
		input_box.columnconfigure((0, 1), weight=1)

		self.subject_menu = tk.OptionMenu(input_box, self.tk_selected_subject, *self.subjects)
		self.subject_menu.grid(row=0, column=0, sticky='nsew')

		subject_settings = tk.Button(input_box, text='Subjects...', command=lambda: self._open_settings_window())
		subject_settings.grid(row=0, column=1, sticky='nsew')

		name_entry = tk.Entry(input_box, textvariable=self.tk_book_name)
		name_entry.grid(row=1, column=0, sticky='nsew')

		save_button = tk.Button(input_box, text='Save', command=lambda: self._save_image_action())
		save_button.grid(row=1, column=1, sticky='nsew')

		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

	def load_frame(self, image_pil):
		"""
		Method is using provaded pil image to update camera view label
		"""

		self.camera_view.configure(image=image_pil)
		self.camera_view.image = image_pil

	def _save_image_action(self):
		"""
		Method is used to call controller method to save file
		"""

		subject = self.tk_selected_subject.get()
		book_name = self.tk_book_name.get()
		self.controller.save_image_from_camera(book_name, subject)

	# TREE VIEW
	def create_treeview_view(self):
		"""
		Creating treeview
		"""

		treeview_frame = tk.Frame()

		tk.Label(treeview_frame, text='Saved books:', font=self.bold_font).pack(anchor='w')

		# Path frame
		path_frame = tk.Frame(treeview_frame)
		path_frame.pack(pady=5, fill='x')

		select_path_button = tk.Button(path_frame, text='Select directory', command=lambda: self.ask_for_path())
		select_path_button.pack(side='left')

		path_label = tk.Label(path_frame, textvariable=self.tk_path)
		path_label.pack(side='left', expand=True, fill='x')

		self.treeview = ttk.Treeview(treeview_frame, selectmode='browse')

		self.treeview.configure(columns=('subject', 'counter'))
		self.treeview.heading('#0', text='Name')
		self.treeview.heading('subject', text='Subject')
		self.treeview.heading('counter', text='Counter')

		self.treeview.pack(fill='both', expand=True)

		treeview_frame.pack(side='left', fill='y', expand=True, padx=20, pady=20)
		ttk.Separator(self, orient='vertical').pack(side='left', fill='y')

		self.treeview.bind('<<TreeviewSelect>>', self.book_selected)

	def book_selected(self, e):
		for i in self.treeview.selection():
			if self.treeview.item(i)['values']:
				selected_book_values = self.treeview.item(i)['values']
				self.controller.preview_image(selected_book_values[2])

	def load_data_to_treeview(self, file_list):
		"""
		Loading data from file_list to treeview
		"""

		file_list = sorted(file_list, key=lambda file: (file['subject'], file['name'], file['number']))

		for file in file_list:
			self.add_data_to_treeview(file)

	def add_data_to_treeview(self, file):
		"""
		Method is adding file to treeview
		"""

		name = file['name']
		subject = file['subject']
		number = file['number']
		raw_name = f'SCAN_{subject}_{name}_{number}.png'

		matched = False

		for child in self.treeview.get_children():
			element = list(self.treeview.item(child).values())

			if name == element[0]:
				self.treeview.insert(parent=child, index=tk.END, values=(subject, number, raw_name))
				matched = True

		if not matched:
			row = self.treeview.insert(parent='', index=tk.END, text=name)
			self.treeview.insert(parent=row, index=tk.END,  values=(subject, number, raw_name))

	def clear_treeview(self):
		"""
		Removing all elements from treeview
		"""

		for children in self.treeview.get_children():
			self.treeview.delete(children)

	def load_preview(self, image_pil):
		self.preview.configure(image=image_pil)
		self.preview.image = image_pil

	# IMPORT VIEW
	def create_preview_view(self):
		"""
		Creating input view
		"""


		input_frame = tk.Frame(self, width=324)
		input_frame.pack_propagate(False)

		tk.Label(input_frame, text='Preview:', font=self.bold_font).pack(anchor='w')

		self.preview = tk.Label(input_frame)
		self.preview.pack(fill='both', expand=True)

		input_frame.pack(side='left', padx=20, pady=20, fill='both')
