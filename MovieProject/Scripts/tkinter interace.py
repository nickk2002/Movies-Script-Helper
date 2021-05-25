import tkinter as tk

window = tk.Tk(className="My Window")
window.geometry("500x500")
border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}
for (key, value) in border_effects.items():
    frame = tk.Frame(relief=value, borderwidth=5)
    text = tk.Label(text="Some text here" + key, master=frame)
    text.pack(side=tk.LEFT)
    # frame.pack()

# for i in range(3):
#     # window.columnconfigure(i,weight=2,minsize=200)
#     # window.rowconfigure(i,weight=1,minsize=200)
#     for j in range(3):
#         frame = tk.Frame(master=window,relief=tk.RAISED, borderwidth=1)
#         frame.grid(row=i, column=j)
#         label = tk.Label(master=frame, text=f"Hi am here {i, j}")
#         # label.pack(padx=25,pady=25)

# frame = tk.Frame(master=window,relief=tk.RAISED,width=100,bg='red')
# frame.pack(fill=tk.Y,side=tk.LEFT)
label = tk.Label(text="Hi am in a grid in a frame",width=500,bg='yellow')
# label.grid(row=0,column=0,sticky='nsew')
# label.grid(row=0,column=0)
label.pack()

window.mainloop()
