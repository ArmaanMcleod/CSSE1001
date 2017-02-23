#!/usr/bin/env python3
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Username: s4396043
#
#   Student Name: Armaan Dhaliwal-McLeod
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here
      
class AnimalData(object):
    """ Animal Data is class which has no arguements and stores the animals loaded from
    the AnimalDataSet respectively.

    stored data structures can be from this class
    """
    def __init__(self):
        """ Constructor for AnimalData(). Creates a dictionary, two lists and a tuple
        to store data inputs.

        Constructor() -> None
        """
        self._data = {}
        self._animalNames = []
        self._animalSelect = []
        self._ranges = ()

    def load_data(self,filename):
        """ Returns data from AnimalDataSet into a class dictionary.

        AnimalData.load_data(str) -> None
        """
        animal_name = filename.split('.')[0]
        animal = AnimalDataSet(filename)
        if not animal.get_name() in self.get_animal_names() and len(self._animalNames) < 8:
            self._animalNames.append(animal_name)
            self._animalSelect.append(True)
            self._data[animal_name] = animal

    def get_data(self):
        """Returns a dictionary containing the data.

        AnimalData.get_data() -> {}
        """
        return self._data

    def get_animal_names(self):
        """Returns a list of names of the animals that have been called.

        AnimalData.get_animal_names() -> list(str)
        """
        return self._animalNames

    def get_animal(self,animal):
        """ Returns an object of the AnimalDataSet class so it's functions are
        accessible.

        AnimalData.get_animal(str) -> object
        """
        return self._data[animal]

    def is_selected(self,index): 
        """ Returns a boolean to determine if the indexth animal is to displayed.

        AnimalData.is_selected(int) -> Boolean
        """
        return self._animalSelect[index]

    def select(self,index):
        """ Sets the indexth data set, indicates that the animal to be displayed.

        AnimalData.select(int) -> None
        """
        self._animalSelect[index] = True
        
    def deselect(self,index):
        """ Cleats the indexth data set, indicating that the animal should not be
        displayed.

        Animal.deselect(int) -> None
        """
        self._animalSelect[index] = False

    def get_ranges(self):
        """ Returns a 4-tuple in the form of
        (min_height, max_height, min_weight, max_weight).

        AnimalData.get_ranges() -> tuple(float, float, float, float)
        """
        
        (min_height, max_height, min_weight, max_weight) = (None,None,None,None)
        height = ()                            
        weight = ()
        for index, select in list(enumerate(self._animalSelect)):
            if select == True:
                i = self._animalNames[index]
                animal = self.get_animal(i)
                height_range = animal.get_height_range()
                weight_range = animal.get_weight_range()
                for x,y in zip(height_range,weight_range):
                    height = height + height_range
                    weight = weight + weight_range
                min_height = min(height)
                max_height = max(height)
                min_weight = min(weight)
                max_weight = max(weight)
                
        ranges = (min_height, max_height, min_weight, max_weight)
        return ranges
        
    def to_tabbed_string(self,index):
        """ Returns a padded string summarising the indexth data sets.

        AnimalData.to_tabbed_string(int) -> string
        """
        names = self._animalNames[index]
        animalObject = self._data[names]
        count = len(animalObject.get_data_points())
        selected = "Visible"
        notselected = "Hidden"
        if self._animalSelect[index] == True:
            return LABEL_FORMAT.format(names,count,selected)
        else:
            return LABEL_FORMAT.format(names,count,notselected)
                    
class Plotter(tk.Canvas):
    """ Plotter is a class responsible for plotting data points, creating a cursor
    with mouse motion and displaying canvas coordinates of cursor. This class inherits
    from tk.Canvas.
    """
    def __init__(self, master, AnimalData):
        """ Constructor(object) -> Nonetype
        """
        super().__init__( master, bg = "white")
        
        self._AnimalData = AnimalData
        self.bind("<Configure>",self.resize)
        self.bind("<Motion>",self.cursor_motion)
        self.bind("<Leave>",self.clear_cursor)
        self.label = tk.Label(master, text = "")
        self.label.pack(anchor = tk.N, fill = tk.X)
        self._height = self.winfo_height()
        self._width = self.winfo_width()
        self.coord_save = None
        self.centrepoint = 2.5

    def clear_cursor(self,event):
        """ Clears cursor from the canvas and updates label as none when cursor
        leaves canvas.
        """
        self.delete("cursor")
        self.label.config(text = "")

    def canvas_size(self):
        """ Returns the size of the canvas.

        Plotter.canvas_size -> tuple(int)
        """
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        return self.height, self.width

    def redraw(self):
        """ Updates data points to draw and displays them on canvas.

        Plotter.redraw() -> Nonetype
        """
        self.delete(tk.ALL)
        min_height = self._AnimalData.get_ranges()[0]
        max_height = self._AnimalData.get_ranges()[1]
        min_weight = self._AnimalData.get_ranges()[2]
        max_weight = self._AnimalData.get_ranges()[3]
        if min_height != None or max_height != None or min_weight != None or max_weight != None:
            self.coord_save = CoordinateTranslator(self.winfo_width(), self.winfo_height(),min_height,max_height,min_weight,max_weight)
            count = 0
            for name in self._AnimalData.get_animal_names():
                self.filename = name + '.csv'
                self._Data = AnimalDataSet(self.filename)
                self._Data.get_data_points()
                if self._AnimalData.is_selected(count):
                    animal = self._AnimalData.get_animal(name)
                    animal_data =self._Data.get_data_points()
                    for height,weight in animal_data:
                        x,y = (self.coord_save.get_coords(height,weight))
                        xval1,yval1 = (x + self.centrepoint,y + self.centrepoint)
                        xval2,yval2= (x - self.centrepoint,y - self.centrepoint)
                        colours = COLOURS[count % len(COLOURS)]
                        self.create_rectangle(xval2,yval2,xval1,yval1,outline = colours,\
                                              fill = colours, tag = "point" )
                count = count + 1
        
    def resize(self, event):
        """Redraws the updates the canvas label when canvas is resized.

        Plotter(Event object).resize -> None
        """
        self.redraw()
        

    def cursor_motion(self, e):
        """Responsible for projecting coordinates of mouse by displaying the height
        and weight of each animal respectively. Updates the label and creates a crosshair
        at the canvas location of the mouse. Recieves e.x,.ey from points shown.

        cursor_moution(event object) -> canvas coordinates and label text
        """
        self.delete("cursor")
        ranges = self._AnimalData.get_ranges()
        min_height = ranges[0]
        max_height = ranges[1]
        min_weight = ranges[2]
        max_weight = ranges[3]
        if min_height != None or max_height != None or min_weight != None or max_weight != None:
            horizontal = (e.x, 0, e.x, self.winfo_height())
            vertical = (0, e.y, self.winfo_width(),e.y)
            self.create_line(horizontal, tag = 'cursor')
            self.create_line(vertical, tag = 'cursor')
            
            ct = CoordinateTranslator(self.winfo_width(), self.winfo_height(),min_height,max_height,min_weight,max_weight)
            Height = ct.get_height(e.x)
            Weight = ct.get_weight(e.y)
            round_h = round(Height,2)
            round_w = round(Weight,2)
            self.label.config(text = "Height:{0}cm, Weight:{1}kg".format(round_h,round_w)) 
                
class SelectionBox(tk.Listbox):
    """ An interactive tkinter Listbox responsible for displaying a list of animals.
    """
    def __init__(self,master,plotter,AnimalData):
        """ A Selectionbox class which handles the master class, AnimalData and Plotter class.
        Selectionbox will inherit from tk.Listbox.

        Constructor(object) -> Nonetype
        """
        super().__init__(master, font = SELECTION_FONT)
        self._Data = AnimalData
        self._plotter = plotter
        self._items = []

    def add_it(self,pos,animal):
        """ Displays Listbox items in terms of the indexth animal. Returns error
        if limit of available animals is exceeded.

        Selectionbox.add_it(object, object) -> Nonetype
        """
        try:
            self._position = pos
            self._animal_str = animal
            if pos < 8:
                self.insert(pos,animal)
                self._items.append(animal)
                self.itemconfig(pos,fg=COLOURS[pos])
            elif pos >= 8:
                return
        except IndexError:
            messagebox.showerror('Index Error','Limit of indexes exceeded.')
             
class AnimalDataPlotApp(object):
    """ Top Level GUI class. Mananges AnimalData, Plotter and Selectionbox and
    is the main layout for the program.

    AnimalDataPlotApp -> GUI Application
    """
    def __init__(self, master):
        """ Constructor(object) -> Nonetype
        """
        self._master = master
        master.title("Animal Data Plot App")
        master.geometry("800x400")
        self._AnimalData = AnimalData()

        self._frame = tk.Frame(master)
        self._frame.pack(side = tk.RIGHT,expand = True, fill = tk.BOTH) 
        self._canvas = Plotter(self._frame, self._AnimalData)
        self._canvas.pack(side = tk.LEFT,expand = True, fill = tk.BOTH)

        self._list_frame = tk.Frame(self._master)
        self._list_frame.pack(side = tk.LEFT, fill = tk.BOTH)

        animal_label = tk.Label(self._list_frame, text = "Animal Data Sets")
        animal_label.pack(side = tk.TOP)

        bframe = tk.Frame(self._list_frame)
        bframe.pack(side = tk.TOP)

        button1 = tk.Button(bframe, text = "Select", command = self.selector)
        button1.pack(side = tk.LEFT, expand = True, fill = tk.X, ipadx = 40)
        button2 = tk.Button(bframe, text = "Deselect", command = self.deselector)
        button2.pack(side = tk.LEFT, expand = True, fill = tk.X, ipadx = 40)

        self._listbox = SelectionBox(self._list_frame ,self._canvas,self._AnimalData)
        self._listbox.pack(side = tk.LEFT, fill = tk.BOTH, expand =True)
        
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar)
        master.config(menu = menubar)
        menubar.add_cascade(label = "File", menu = filemenu)
        filemenu.add_command(label = "Open", command = self.open_file)

        self.i = 0
        self._data = []
        
    def open_file(self):
        """ Opens a file that can be used in the application.

        AnimalDataPlotApp() -> None
        """
        path = filedialog.askopenfilename()
        directory = str(path)
        filename = directory.split('/')[-1]
        if filename[-4:] == '.csv':
            try:
                self._data.append(load_data_set(filename))
                self._AnimalData.load_data(filename)
                if len(self._AnimalData._animalNames) > self.i :
                    self.animal = self._AnimalData.to_tabbed_string(-1)
                    self._listbox.add_it(self.i,self.animal)                 
                    self._canvas.redraw()
                    self.i += 1
                    
            except ValueError:
                messagebox.showerror('File Error.', 'The file selected contains invalid data : ' + filename +\
                                     '. Selected file contains a value error.')
            except IndexError:
                messagebox.showerror('File Error.', 'The file selected contains invalid data :' + filename +\
                                     '. Selected file contains an index error.')
            
            except Exception:
                messagebox.showerror('File Error.', 'The file selected cannot be opened :' + filename  +\
                                     '. Please check the file before continuing.')
        
            except IOError:
                messagebox.showerror('File Error.','The file selected is undreadable :' + filename  +\
                                     '. Please check the file permissions before continuing.')
        
            except FileNotFoundError:
                messagebox.showerror('File Error.', 'The file selected cannot be found :' + filename  +\
                                     '. Please check the file location and try again.')
                                     
        elif filename == "":
            return
       
        else:
            messagebox.showerror('File Error.','File selected: ' + filename + '. The file selected must contain a' +\
                                 ' .csv extension.' + ' Please select another file.')
            return
    
    def selector(self):
        """ Updates the selected state of the indexth animal to True and updates the
        program.

        Selectionbox.select() -> None
        """
        try:
            self.selection = int(self._listbox.curselection()[0])
            self.flag_chk = self._AnimalData.is_selected(self.selection)
            if self.flag_chk is False:
                self._AnimalData.select(self.selection)
                self.ani_string = self._AnimalData.to_tabbed_string(self.selection)
                self._listbox.delete(self.selection, None)
                self._listbox.add_it(self.selection,self.ani_string)
                self._listbox.itemconfig(self.selection,fg=COLOURS[self.selection % len(COLOURS)])
                self._canvas.redraw()
        except IndexError:
            messagebox.showerror("Selection Error","No Index selected: Please select an index.")

    def deselector(self):
        """ Updates the selected state of the indexth animal to False and updates the
        program.

        Selectionbox.deselect() -> None
        """
        try:
            self.selection = int(self._listbox.curselection()[0])
            self.flag_chk = self._AnimalData.is_selected(self.selection)
            if self.flag_chk:
                self._AnimalData.deselect(self.selection)
                self.ani_string = self._AnimalData.to_tabbed_string(self.selection)
                self._listbox.delete(self.selection, None)
                self._listbox.add_it(self.selection,self.ani_string)
                self._listbox.itemconfig(self.selection,fg=COLOURS[self.selection % len(COLOURS)])
                self._canvas.redraw()
        except IndexError:
                messagebox.showerror("Selection Error","No Index selected: Please select an index.")
                                     
        
##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

def main():
    root = tk.Tk()
    app = AnimalDataPlotApp(root)
    root.geometry("800x400")
    root.mainloop()

if __name__ == '__main__':
    main()
