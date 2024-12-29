from PIL import Image, ImageTk

from model import Model
from view import View
import os

class Controller:

	def __init__(self):
		self.settings = AppSettings()

		self.model = Model(self.settings.get_files_path())
		self.view = View(self)

		self.update_image_from_camera()

	def main(self):
		self.load_tree_view()
		self.view.main()

	def load_tree_view(self):
		file_list = self.model.get_saved_images()
		self.view.load_data_to_treeview(file_list)

	def update_image_from_camera(self):
		"""
		Method is getting frame from camera. In case we're not able to get data we're using default
		picture. Method is calling itself to still keep current image
		"""

		try:
			image_pil = self.model.get_pil_image_from_camera()
		except:
			default_image_path = "Image/noSignal.png"

			# I'm using (324, 576) because it's resolution of image sending by
			# my method and my camera
			image_pil = Image.open(default_image_path).resize((324, 576))
			image_pil = ImageTk.PhotoImage(image_pil)

		self.view.load_frame(image_pil)

		self.view.after(1, self.update_image_from_camera)

	def save_image_from_camera(self, filename):
		"""
		Method is saving frame from camera and then update treeview
		"""
		if filename == '':
			return
		
		name, number = self.model.save_image(filename)
		self.view.add_data_to_treeview(name, number)

	# SETTINGS
	def update_files_path(self, path):
		self.settings.update_files_path(path)
		self.view.set_path(path)
		self.model.app_path = path

		self.view.clear_treeview()
		self.load_tree_view()

	def get_files_path(self):
		return self.settings.get_files_path()

class AppSettings:
	def __init__(self):
		self.path = '/Users/lukaszmichalak/myApp/ScanBook'

	def update_files_path(self, path):
		self.path = path

	def get_files_path(self):
		return  self.path

if __name__ == '__main__':

	app = Controller()
	app.main()