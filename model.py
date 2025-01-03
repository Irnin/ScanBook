from collections import defaultdict

import cv2
import os
import shutil
import py7zr
from PIL import Image, ImageTk

class Model:
	def __init__(self, path):
		self.camera = cv2.VideoCapture(0)
		self.app_path = path

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

	def save_image(self, book_name, subject):
		"""
		Method is saving current frame with provided filename. To protect from overwriting method is
		adding counter.

		Returns tuple of file name and counter to add it into treeview
		"""

		image = self.get_image_from_camera()
		image = self.rotate_image(image)

		image_counter = self.get_number_of_files(book_name)

		filename = f'SCAN_{subject}_{book_name}_{image_counter}.png'
		path = os.path.join(self.app_path, filename)
		cv2.imwrite(path, image)

		file = dict()
		file['name'] = book_name
		file['subject'] = subject
		file['number'] = image_counter

		return file

	def get_number_of_files(self, filename):
		"""
		Method is checking how many files we have with provided filename
		"""

		image_counter = 0

		for file in os.listdir(self.app_path):
			if not file.startswith('SCAN_'):
				continue

			if not filename in file:
				continue

			decoded_file = self._disassembly_filename(file)

			if int(decoded_file['number']) > image_counter:
				image_counter = int(decoded_file['number'])

		return image_counter + 1

	def _disassembly_filename(self, filename):
		"""
		Method is using regex to get name and number from provided file name
		"""
		file = dict()
		file['original'] = filename
		filename = filename.removesuffix('.png')
		disassembled_filename = filename.split('_')

		file['name'] = disassembled_filename[2]
		file['subject'] = disassembled_filename[1]
		file['number'] = disassembled_filename[3]
		file['short_name'] = fr"{file['name']}_{file['number']}.png"

		return file

	def get_saved_images(self):
		"""
		Method is returning list of saved images

		Files are saved with template:
		SCAN_[SUBJECT]_NAME_COUNTER.png
		"""

		files_list = []

		for file_name in os.listdir(self.app_path):

			# Skip files that wasn't created by our program
			if not file_name.startswith('SCAN_'):
				continue

			file = self._disassembly_filename(file_name)

			files_list.append(file)

		return files_list

	def export_saved_images(self):

		files = self.get_saved_images()

		# Reorganizing files
		for file in files:
			root = self.app_path

			original_path = fr"{root}/{file['original']}"
			new_path = fr"{root}/export/{file['subject']}/{file['name']}/{file['short_name']}"

			os.makedirs(os.path.dirname(new_path), exist_ok=True)
			shutil.move(original_path, new_path)

		# Packing it
		folder_path = fr'{self.app_path}/export/'
		output_path = fr'{self.app_path}/ScannedBooks.7z'

		with py7zr.SevenZipFile(output_path, 'w') as archive:
			archive.writeall(folder_path, os.path.basename(folder_path))

		# Removing old files
		shutil.rmtree(folder_path)