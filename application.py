from tkinter import *
import nutrition
import tkinterAutoEntry

connector = nutrition.Connector()

#Nutrients to track. See NUTR_DEF.txt in the Data folder for additional nutrients.
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

ingredientdata = {}

root = Tk()
root.title('Nutrition Calculator')

frame = Frame(root)
label = Label(frame, text='Search Food Database:')
search = tkinterAutoEntry.AutoCompleteEntry(frame, width=75)

frame.grid(row=0, column=0)
label.grid(row=0, column=1)
search.grid(row=0, column=2)

def add():
    start_row = 2
    grid_row = len(ingredientdata)
    food = search.text.get()
    show_row = table[grid_row]
    
    show_row[0].grid(row=grid_row+start_row, column=1)
    show_row[1].config(text=food)
    show_row[1].grid(row=grid_row+start_row, column=2)
    show_row[2].grid(row=grid_row+start_row, column=3)
    
    dbnum = search.selection[0]
    table[grid_row].append(dbnum)
    nutinfo = connector.nutData(dbnum)
    temp =  {}
    
    #1st and 2nd indexes are nutrient number and value
    for row in nutinfo:
        if row[1] in nutrlist:
            temp.update({row[1]: row[2]})
    
    ingredientdata.update({dbnum: temp})
    
    search.selection = '';
    search.text.set('')

def delete(Event):
    widget = Event.widget
    index = 0
    for x in table:
        if widget in x:
            index = table.index(x)
            
    row = table[index]
    row[0].grid_forget()
    row[1].config(text='')
    row[1].grid_forget()
    row[2].grid_forget()
    ingredientdata.pop(row[3])
    row.remove(row[3])
    table.insert(-1, table.pop(index))
    
    for x in range(index, len(table)):
        if table[x][1].cget('text'):
            table[x][0].grid(row=x+2, column=1)
            table[x][1].grid(row=x+2, column=2)
            table[x][2].grid(row=x+2, column=3)
    
table = []    
for x in range(0,15):
    button = Button(frame, bitmap='error')
    button.bind('<Button-1>', delete)
    label = Label(frame, width=75, anchor=W)
    spin = Spinbox(frame, width=7, from_=0, to=10000)
    temp = [button, label, spin]
    table.append(temp)

addFood = Button(frame, text='Add Food', command=add)
addFood.grid(row=0, column=3)


nutrientlabel = []
current = []
unitlabel = []
targetlabel = []
nut = nutrition.Connector()
rindex = 0
for x in nutrlist.values():
    rstring = x[0]
    nutrientlabel.append(Label(frame, width=20, anchor=E, text=x[0], pady=1))
    unitlabel.append(Label(frame, width=3, text=x[1], anchor=W))
    targetlabel.append(Label(frame, width=3, text=x[1], anchor=W))
    
    nutrientlabel[rindex].grid(row=rindex+1, column=4)
    unitlabel[rindex].grid(row=rindex+1, column=6)
    targetlabel[rindex].grid(row=rindex+1, column=8)
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
