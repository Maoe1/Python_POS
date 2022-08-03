#frames
import tkinter as tk
#Set the geometry of frame

root = tk.Tk()
root.title("Gbc Online Store")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

canvas = tk.Canvas(root, width=600, height=350)
canvas.grid(columnspan=6, rowspan=6)


frame1 = tk.Frame(root, bg="#355e3b")
frame2 = tk.Frame(root, bg="#355e3b")
frame3 = tk.Frame(root, bg="#355e3b")
frame4 = tk.Frame(root, bg="#355e3b")
frame5 = tk.Frame(root, bg="#355e3b")

for frame in (frame1, frame2, frame3, frame4, frame5):
    frame.grid(row=0, column=0, sticky="nsew")