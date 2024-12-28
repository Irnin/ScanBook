from PIL import Image, ImageTk

from model import Model
from view import View
import os

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View(self)

		self.update_image_from_camera()

	def main(self):
		file_list = self.model.get_images()
		self.view.load_data_to_treeview(file_list)

		self.view.main()

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
		if filename == '':
			return
		
		self.model.save_image(filename)

if __name__ == '__main__':

	app = Controller()
	app.main()