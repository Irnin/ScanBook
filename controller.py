import pickle

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

from model import Model
from view import View
import os

class Controller:

	def __init__(self):
		self.settings = AppSettings()

		self.model = Model(self.settings.get_files_path())
		self.view = View(self, self.settings.get_subjects())

		self.update_image_from_camera()

		# BINDS

		# Clicking on image will reset camera loop
		self.view.camera_view.bind('<Button-1>', lambda e: self.update_image_from_camera())

	def main(self):
		self.load_tree_view()
		self.view.main()

	def load_tree_view(self):
		"""
		Method reads files in directory and then display it in treeview
		"""

		file_list = self.model.get_saved_images()
		self.view.load_data_to_treeview(file_list)

	def update_image_from_camera(self):
		"""
		Method is getting frame from camera. In case we're not able to get data we're using default
		picture. Method is calling itself to still keep current image
		"""

		try:
			if not self.view.winfo_exists():
				return

			image_pil = self.model.get_pil_image_from_camera()
		except:
			default_image_path = "image/noSignal.png"

			# I'm using (324, 576) because it's resolution of image sending by
			# my method and my camera
			image_pil = Image.open(default_image_path).resize((324, 576))
			image_pil = ImageTk.PhotoImage(image_pil)

		self.view.load_frame(image_pil)

		self.view.after(10, self.update_image_from_camera)

	def save_image_from_camera(self, book_name, subject):
		"""
		Method is saving frame from camera and then update treeview
		"""

		if book_name == '':
			return
		
		file = self.model.save_image(book_name, subject)
		self.view.add_data_to_treeview(file)

	def preview_image(self, file_name):
		full_file_path = f'{self.settings.get_files_path()}/{file_name}'

		image_pil = Image.open(full_file_path).resize((324, 576))
		image_pil = ImageTk.PhotoImage(image_pil)

		self.view.load_preview(image_pil)

	# SETTINGS
	def update_files_path(self, path):
		"""
		Method is called when user change path to work with.
		Updates settings and reload treeview
		"""

		self.settings.update_files_path(path)
		self.view.set_path(path)
		self.model.app_path = path

		self.view.clear_treeview()
		self.load_tree_view()

	def get_files_path(self):
		return self.settings.get_files_path()

	def remove_subject(self, subject):
		subjects = self.settings.remove_subject(subject)

		self.reload_subjects_in_view(subjects)

	def add_subject(self, subject):
		subjects = self.settings.add_subject(subject)

		self.reload_subjects_in_view(subjects)

	def reload_subjects_in_view(self, subjects):
		self.view.load_subjects(subjects)
		self.view.load_subjects_to_settings_view()
		self.view.load_subjects_to_input_view()

class AppSettings:
	"""
	Class was created to simply manage app settings and save them
	"""

	def __init__(self):
		directory = os.path.expanduser("~/myApp/ScanBook")
		os.makedirs(directory, exist_ok=True)
		self.save_file_path = os.path.join(directory, "settings.pkl")

		self.load()

	# Save settings
	def save(self):
		"""
		Save data from model to file
		"""
		with open(self.save_file_path, 'wb') as file:
			pickle.dump(self, file)

	def load(self):
		"""
		Load model data from file
		"""

		try:
			with open(self.save_file_path, 'rb') as file:
				loaded_model = pickle.load(file)
				self.path = loaded_model.path
				self.subjects = loaded_model.subjects
		except Exception as e:
			print(e)
			print("Can not load")
			self.path = '/Users/lukaszmichalak/myApp/ScanBook'
			self.subjects = ['Chemistry', 'Biology']

	# File path
	def update_files_path(self, path):
		self.path = path
		self.save()

	def get_files_path(self):
		return  self.path

	# Subjects
	def get_subjects(self):
		"""
		Returns subjects
		"""
		return self.subjects

	def add_subject(self, subject) -> [str]:
		"""
		Adding subject to array and returns it
		"""
		self.subjects.append(subject)
		self.save()

		return self.subjects

	def remove_subject(self, subject):
		"""
		Method is trying to remove provided subject from array and then returns current list
		"""
		try:
			self.subjects.remove(subject)
			self.save()
		except:
			print(f'Could not remove subject {subject} from list')

		return self.subjects

if __name__ == '__main__':

	app = Controller()
	app.main()