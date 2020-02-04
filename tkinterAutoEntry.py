from threading import Timer
from tkinter import *
import nutrition

class AutoCompleteEntry(Entry):
    
    def __init__(self, *args, **kwargs):
        super(AutoCompleteEntry,self).__init__(*args, **kwargs)
        self.text = self['textvariable'] = StringVar()
        self.nutr = nutrition.Connector()
        self.lbox = '' #Listbox() holder
        self.timer = ''
        self.selection = '' #RowResult Object holder
        self.text.trace('w',self.initTimer)
        
    def timerSearch(self):
        if not self.text.get():
            self.lbox.destroy()
            
        elif not self.selection or self.selection[2] != self.text.get():
            scrollbar = Scrollbar()
            self.lbox = Listbox(yscrollcommand=scrollbar.set,width=100)
            self.result = self.nutr.foodSearch(self.text.get())
            if self.result:
                self.lbox.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                self.lbox.bind('<Button-1>', self.select)
                self.lbox.delete(0,END)
                for row in self.result:
                    self.lbox.insert(END,row[2])
                scrollbar.config(command=self.lbox.yview)
        else:
            self.lbox.destroy()

    def initTimer(self,*args):
        if not self.text:
            self.lbox.destroy()
            return
        
        if self.timer:
            self.timer.cancel()
        
        self.timer = Timer(1.5, self.timerSearch)
        self.timer.start()

    def select(self, Event):
        choice = self.lbox.nearest(Event.y)
        self.selection = self.result[choice]
        self.text.set(self.selection[2])
        self.lbox.destroy()
                
