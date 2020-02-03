from tkinter import *
import nutrition
import tkinterAutoEntry

root = Tk()
root.title('Nutrition Calculator')
searchFrame = Frame(root, height=200, width=100)
searchFrame.pack()
label = Label(searchFrame, text="Search Food Database:")
label.pack()
search = tkinterAutoEntry.AutoCompleteEntry(searchFrame, width=100)
search.pack()
def add():
    lb.insert(END,search.text.get())
    search.selection = '';
    search.text.set('')
lb = Listbox(width=75)
addFood = Button(searchFrame, text='Add Food', command=add)
addFood.pack()
lb.pack()

root.mainloop()

