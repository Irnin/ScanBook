from model import Model
from view import View

class Controller:

	def __init__(self):
		self.model = Model()
		self.view = View(self)

	def main(self):
		self.view.main()

if __name__ == '__main__':
	app = Controller()
	app.main()