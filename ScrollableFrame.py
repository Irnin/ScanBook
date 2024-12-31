import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
	def __init__(self, container, *args, **kwargs):

		super().__init__(container, *args, **kwargs)

		self.canvas = tk.Canvas(self)
		self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.scrollbar.set)
		self.scrollable_frame = ttk.Frame(self.canvas)
		self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y", padx=10)

		self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
		self.canvas.bind("<Configure>", self._on_canvas_configure)
		self.bind_all("<MouseWheel>", self._on_mouse_wheel)

	def _on_frame_configure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def _on_canvas_configure(self, event):
		self.canvas.itemconfig(self.scrollable_window, width=event.width)

	def _on_mouse_wheel(self, event):
		self.canvas.yview_scroll(-1 * event.delta, "units")

	def clear_frame(self):
		for widget in self.scrollable_frame.winfo_children():
			widget.destroy()
