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
		Get pure image from camera
		"""
		result, image = self.camera.read()

		return image

	def rotate_image(self, image):
		"""
		Rotating image
		"""
		image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
		return image

	def resize_image(self, image):
		"""
		Resizing image
		"""
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
		"""
		Method is reading frame from camera. Converting it with special method and then converting to PIL image
		"""
		image = self.get_image_from_camera()
		image = self.convert_image(image)

		image_pil = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert colors
		image_pil = Image.fromarray(image_pil)  # Convert to PIL format
		image_pil = ImageTk.PhotoImage(image_pil)  # Convert to ImageTk format

		return image_pil

	def save_image(self, provided_filename):
		"""
		Method is saving current frame with provided filename. To protect from overwriting method is
		adding counter.

		Returns tuple of file name and counter to add it into treeview
		"""
		image = self.get_image_from_camera()
		image = self.rotate_image(image)

		image_counter = self.get_number_of_files(provided_filename)

		filename = f'{provided_filename}_{image_counter}.png'
		path = os.path.join(self.app_path, filename)
		cv2.imwrite(path, image)

		return (provided_filename, image_counter)

	def get_number_of_files(self, filename):
		"""
		Method is checking how many files we have with provided filename
		"""
		image_counter = 0

		regex = f'^{filename}_\d+\.png$'

		for root, dirs, files in os.walk(self.app_path):
			for file in files:
				if re.match(regex, file):
					image_counter += 1

		return image_counter

	def disassembly_filename(self, filename):
		"""
		Method is using regex to get name and number from provided file name
		"""
		regex_name = re.compile(r"^(.*?)_")
		regex_number = re.compile(r"_(\d+)\.png$")

		name_match = regex_name.search(filename)
		name = name_match.group(1) if name_match else None

		number_match = regex_number.search(filename)
		number = int(number_match.group(1)) if number_match else None

		return name, number

	def get_saved_images(self):
		"""
		Method is returning list of saved images
		"""
		files_list = defaultdict(list)

		for root, dirs, files in os.walk(self.app_path):
			for file in files:
				if file[0] == '.':
					continue

				name, number = self.disassembly_filename(file)

				files_list[name].append(number)

		return files_list
