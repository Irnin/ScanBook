import tkinter as tk
from tkinter import ttk

class View(tk.Tk):
	def __init__(self, controller):
		super().__init__()

		self.title('ScanBooks')
		self.geometry('500x600')

		self.controller = controller

	def main(self):
		self.mainloop()