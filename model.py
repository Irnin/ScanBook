import cv2
from PIL import Image, ImageTk

class Model:
	def __init__(self):
		self.camera = cv2.VideoCapture(0)

	def get_image_from_camera(self):
		"""
		Method is getting image from camera, converting it and returning as PIL image
		"""

		result, image = self.camera.read()

		# RESIZING
		scale_percent = 30
		width = int(image.shape[1] * scale_percent / 100)
		height = int(image.shape[0] * scale_percent / 100)
		dim = (width, height)
		image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

		# ROTATING
		image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

		# CONVERTING TO PIL IMAGE
		image_pil = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert colors
		image_pil = Image.fromarray(image_pil)  # Convert to PIL format
		image_pil = ImageTk.PhotoImage(image_pil)  # Convert to ImageTk format

		return image_pil
