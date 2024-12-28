from collections import defaultdict

import cv2
import os
import re
from PIL import Image, ImageTk

class Model:
	def __init__(self):
		self.camera = cv2.VideoCapture(0)
		self.app_path = '/Users/lukaszmichalak/myApp/ScanBook'

	def get_image_from_camera(self):
		"""
		Get image from camera
		"""
		result, image = self.camera.read()

		return image

	def rotate_image(self, image):
		image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
		return image

	def resize_image(self, image):
		# RESIZING
		scale_percent = 30
		width = int(image.shape[1] * scale_percent / 100)
		height = int(image.shape[0] * scale_percent / 100)
		dim = (width, height)
		image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

		return image

	def convert_image(self, image):
		"""
		Update size and orientation of image
		"""

		image = self.resize_image(image)
		image = self.rotate_image(image)

		return image

	def get_pil_image_from_camera(self):
		image = self.get_image_from_camera()
		image = self.convert_image(image)

		image_pil = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert colors
		image_pil = Image.fromarray(image_pil)  # Convert to PIL format
		image_pil = ImageTk.PhotoImage(image_pil)  # Convert to ImageTk format

		return image_pil

	def save_image(self, filename):
		image = self.get_image_from_camera()
		image = self.rotate_image(image)

		image_counter = self.find_images_with_name(filename)

		filename += f'_{image_counter}.png'

		print(filename)
		path = os.path.join(self.app_path, filename)
		cv2.imwrite(path, image)

	def find_images_with_name(self, filename):
		image_counter = 0

		regex = f'^{filename}_\d+\.png$'

		for root, dirs, files in os.walk(self.app_path):
			for file in files:
				if re.match(regex, file):
					image_counter += 1

		return image_counter

	def get_images(self):

		regex_name = re.compile(r"^(.*?)_")
		regex_number = re.compile(r"_(\d+)\.png$")

		files_list = defaultdict(list)

		for root, dirs, files in os.walk(self.app_path):
			for file in files:
				if file[0] == '.':
					continue

				name_match = regex_name.search(file)
				name = name_match.group(1) if name_match else None

				number_match = regex_number.search(file)
				number = int(number_match.group(1)) if number_match else None

				files_list[name].append(number)


		return(files_list)
