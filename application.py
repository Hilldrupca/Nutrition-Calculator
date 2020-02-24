from tkinter import *
from decimal import Decimal
import nutrition
import tkinterAutoEntry

nut = nutrition.Connector()

#Nutrients to track. See NUTR_DEF.txt in the Data folder for additional nutrients.
nutrlist = {'208': ('Calories','kcal'), '204': ('Fats','g'), '605': ('Trans fats','g'),
        '606': ('Saturated fats','g'), '645': ('Monounsaturated fats','g'), '646': ('Polyunsaturated fats','g'),
        '601': ('Cholesterol','mg'), '205': ('Carbohydrates','g'), '291': ('Fiber','g'),
        '203': ('Protein','g'), '320': ('Vitamin A','mcg'), '404': ('Thiamin (B1)','mg'),
        '405': ('Riboflavin (B2)','mg'), '406': ('Niacin (B3)','mg'), '410': ('Pantothenic acid (B5)','mg'),
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
    nutinfo = nut.nutData(dbnum)
    temp = {}
    
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
    row[2].selection_clear()
    row[2].grid_forget()
    ingredientdata.pop(row[3])
    row.remove(row[3])
    table.insert(-1, table.pop(index))
    
    for x in range(index, len(table)):
        if table[x][1].cget('text'):
            table[x][0].grid(row=x+2, column=1)
            table[x][1].grid(row=x+2, column=2)
            table[x][2].grid(row=x+2, column=3)
    
    release(Event)

def release(Event):
    Event.widget.after(10,update)

def update():
    fw = []
    for x in table:
        if x[1].cget('text'):
            #Nutrition information in ingredientdata is per 100 grams
            food = ingredientdata.get(x[3])
            
            y = 0
            for nutr in nutrlist:
                value = food.get(nutr)
                if not value:
                    value = 0
                value = Decimal(value*int(x[2].get())/100)
                fw.insert(y, value)
                y += 1

    for x in range(0,len(current)):
        if not len(fw):
            current[x].config(text='0')
            per[x].config(text='')
        else:
            current[x].config(text='{:.1f}'.format(fw[x]))
            tar = target[x].cget('text')
            if tar and current[x].cget('text'):
                tar = Decimal(tar)
                percent = fw[x]/tar*100
                per[x].config(text='{:.1f}'.format(percent))

table = []    
for x in range(0,15):
    button = Button(frame, bitmap='error')
    button.bind('<Button-1>', delete)
    label = Label(frame, width=75, anchor=W)
    spin = Spinbox(frame, width=7, from_=0, to=10000)
    spin.bind('<ButtonRelease-1>', release)
    temp = [button, label, spin]
    table.append(temp)

addFood = Button(frame, text='Add Food', command=add)
addFood.grid(row=0, column=3)

profile = []
with open('Profiles.txt', newline='\n') as file:
    start = 41
    end = 74
    line_number = 0
    for line in file:
        if line_number >40 and line_number <75:
            value = line.split('=').pop().rstrip()
            profile.append(value)
        line_number += 1
            

nutrientlabel = []
current = []
unitlabel = []
target = []
targetlabel = []
per = []
rindex = 0
for x in nutrlist.values():
    rstring = x[0]
    nutrientlabel.append(Label(frame, width=20, anchor=E, text=x[0]))
    current.append(Label(frame, width = 10, text='0', anchor=E))
    unitlabel.append(Label(frame, width=3, text=x[1], anchor=W))
    target.append(Label(frame, width=10, text=profile[rindex], anchor=E))
    targetlabel.append(Label(frame, width=3, text=x[1], anchor=W))
    per.append(Label(frame, width=10, anchor=E))
    
    nutrientlabel[rindex].grid(row=rindex+1, column=4)
    current[rindex].grid(row=rindex+1, column=5)
    unitlabel[rindex].grid(row=rindex+1, column=6)
    target[rindex].grid(row=rindex+1, column=7)
    targetlabel[rindex].grid(row=rindex+1, column=8)
    per[rindex].grid(row=rindex+1, column=9)
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
