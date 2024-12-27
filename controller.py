from model import Model
from view import View

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.view.main()

	def load_image(self):
		image_pil = self.model.get_image_from_camera()
		self.view.load_frame(image_pil)

if __name__ == '__main__':
	app = Controller()
	app.main()