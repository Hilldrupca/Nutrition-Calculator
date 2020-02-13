from tkinter import *
import nutrition
import tkinterAutoEntry

connector = nutrition.Connector()
nutrlist = {'208': ('Calories','kcal'), '204': ('Fats','g'), '605': ('Trans fats','g'),
        '606': ('Saturated fats','g'), '645': ('Monounsaturated fats','g'), '646': ('Polyunsaturated fats','g'),
        '601': ('Cholesterol','mg'), '205': ('Carbohydrates','g'), '291': ('Fiber','g'),
        '203': ('Protein','g'), '320': ('Vitamin A','mcg'), '404': ('Thiamin (B1)','mg'),
        '405': ('Roboflavin (B2)','mg'), '406': ('Niacin (B3)','mg'), '410': ('Pantothenic acid (B5)','mg'),
        '415': ('Vitamin B6','mg'), '435': ('Folate (B9)','mcg'), '418': ('Vitamin B12','mcg'),
        '401': ('Vitamin C','mg'), '324': ('Vitamin D','IU'), '323': ('Vitamin E','mg'),
        '430': ('Vitamin K','mcg'), '421': ('Choline','mg'), '301': ('Calcium','mg'),
        '312': ('Copper','mg'), '313': ('Fluoride','mcg'), '303': ('Iron','mg'),
        '315': ('Manganese','mg'), '304': ('Magnesium','mg'), '305': ('Phosphorus','mg'),
        '306': ('Potassium','mg'), '317': ('Selenium','mcg'), '307': ('Sodium','mg'),
        '309': ('Zinc','mg')}

ingredientnum = {}

root = Tk()
root.title('Nutrition Calculator')

frame = Frame(root)
label = Label(frame, text='Search Food Database:')
search = tkinterAutoEntry.AutoCompleteEntry(frame, width=75)

frame.grid(row=0, column=0)
label.grid(row=0, column=1)
search.grid(row=0, column=2)

def add():
    lb.insert(END,search.text.get())
    updlist(search.selection[0])
    search.selection = '';
    search.text.set('')
    
def updlist(dbNum):
    data = connector.nutData(dbNum)
    return









lb = Listbox(frame, heigh=25, width=75)    
addFood = Button(frame, text='Add Food', command=add)
addFood.grid(row=0, column=3)
lb.grid(row=2, column=2, rowspan=20)


nutrientlabel = []
current = []
unitlabel = []
nut = nutrition.Connector()
rindex = 0
for x in nutrlist.values():
    rstring = x[0]
    nutrientlabel.append(Label(frame, width=20, anchor=E, text=x[0]))
    unitlabel.append(Label(frame, width=3, text=x[1], anchor=W))
    
    nutrientlabel[rindex].grid(row=rindex+1, column=4)
    unitlabel[rindex].grid(row=rindex+1, column=6)
    rindex += 1

curlabel = Label(frame, width=10, text='Current', anchor=E)
tarlabel = Label(frame, width=10, text='Target', anchor=E)
prctlabel = Label(frame, width=10, text='Percent', anchor=E)
prctpadlabel = Label(frame)
curlabel.grid(row=0, column=5)
tarlabel.grid(row=0, column=7)
prctlabel.grid(row=0, column=9)
prctpadlabel.grid(row=0, column=10, padx=10)

root.mainloop()
