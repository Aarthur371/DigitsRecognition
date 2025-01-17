# Ce programme permet de reconnaitre des chiffres écrits à la main
# en utilisant une classification par la méthode du plus proche voisin,
# les chiffres sont fournis sous forme d'images dont on extrait un vecteur
# qui est ensuite comparé au vecteur de chacune des données d'entrainement
# afin de déterminer les k plus proches voisins

# Imports
import io
import tkinter as tk
from PIL import Image, ImageDraw
import functions

# GUI variables
selected_value = None

# Programm parameters
j=0 #nb of data per figure
fig=10 #nb of figures in the database
k = 4 #nb of neighbors

#----------------GUI events------------------

def on_button_click():
    label.config(text="Button Clicked!")

def on_training_button_click():
    canvas['state'] = tk.DISABLED #disable the drawing until a number is chosen
    label.config(text="Choose which number you want to draw")
    # Configure the listbox
    listbox.delete(0,tk.END) #delete elements in listbox starting from position 0
    numbers = generateList(fig)
    for nb in numbers:
        listbox.insert(tk.END, str(nb))
    # Show the listbox
    listbox.grid(row=1,column=0,rowspan=2)

def on_canvas_click(event):
    # Save the coordinates of the mouse click
    global last_x, last_y
    last_x, last_y = event.x, event.y

def on_canvas_drag(event):
    if(canvas['state']==tk.NORMAL):
        # Draw a line from the last saved coordinates to the current mouse position
        global last_x, last_y
        canvas.create_oval(last_x, last_y, event.x, event.y, width=20)
        last_x, last_y = event.x, event.y

def on_erase_button_click():
    label.config(text="Erased !")
    # Clear all items drawn on the canvas
    canvas.delete("all")

def on_testing_button_click():
    global j
    # Search the figure with the minimum amount of data
    min = 1000
    for i in range (fig): #for figures between 0 and 4
        if(functions.data_index(i)<min):
            min=functions.data_index(i)
    j=min
    canvas['state'] = tk.NORMAL #activate the drawing zone
    label.config(text="Draw a figure")

def on_save_button_click():
    # Save the drawing as a PNG file
    canvas.update()
    listbox.update()
    ps = canvas.postscript(colormode='gray')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    dataName = str(selected_value)+"data"+str(functions.data_index(selected_value)) #increment the name of data (format: nb"data"index)
    img.save("data/"+dataName+".png", format="png")
    txt = "data saved as"+dataName
    label.config(text=txt)
    canvas.delete("all")

def on_guess_button_click():
    canvas.update()
    ps = canvas.postscript(colormode='gray')
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    img.save("tests/drawing.png", format="png") #save the drawing
    testVector = functions.image_to_vector("drawing.png","tests") #transform drawing into a vector
    neigh = functions.find_neighbors(j, k, fig, testVector)
    result = functions.print_result(neigh, fig)
    label.config(text="this is a "+str(result)+" !") #display the result of the prediction

def on_settings_button_click():
    canvas['state'] = tk.DISABLED
    # actualize the field number of data
    labelNbData.config(text="Nb data per figure : " + str(functions.find_min_data_index(fig)))
    # display the frame in the "north" of the cell
    settingsFrame.grid(row=2, column=3, columnspan=3, sticky=tk.N)

def on_selection_changed(event):
    global selected_value
    # Get the index of the selected item
    selected_index = listbox.curselection()[0]
    # Get the value of the selected item
    selected_value= listbox.get(selected_index)
    listbox.grid_forget()
    canvas['state'] = tk.NORMAL
    txt="Draw a "+str(selected_value)+" !"
    label.config(text=txt)

def on_save_param_click():
    global fig,k
    try:
        fig = int(entryNbFig.get())
        k = int(entryNeigh.get())
        label.config(text="Parameters saved")
        settingsFrame.grid_forget()
    except ValueError:
        label.config(text="Invalid values")


# Functions
def generateList(fig):
    figures = []
    for i in range (fig):
        figures.append(i)
    return figures


#--------MAIN PROGRAMM---------

# Create the main application window
app = tk.Tk()
window_width=550
window_height=400
app.geometry(""+str(window_width)+"x"+str(window_height)+"")
app.configure(bg="lightgray")
app.title("Numbers recognition")

# Create a label widget
label = tk.Label(app, text="Hello user",font=("Helvetica",13))
label.grid(row=1,column=1,columnspan=2)

# Create a panel for parameters
settingsFrame = tk.Frame(app)
labelNbFig = tk.Label(settingsFrame, text="Nb figures")
labelNeigh = tk.Label(settingsFrame, text="Nb neighbors")
labelNbData = tk.Label(settingsFrame)
entryNbFig = tk.Entry(settingsFrame)
entryNeigh = tk.Entry(settingsFrame)
btnSaveParam = tk.Button(settingsFrame, text="Save Parameters", command=on_save_param_click)
labelNbFig.grid(row=0,column=0)
labelNeigh.grid(row=1,column=0)
entryNbFig.grid(row=0,column=1)
entryNeigh.grid(row=1,column=1)
labelNbData.grid(row=2,column=0,columnspan=2)
btnSaveParam.grid(row=3,column=0,columnspan=2)

# Create a Listbox widget with single choice
global listbox
listbox = tk.Listbox(app, selectmode=tk.SINGLE, width=3, height=15)  # width/height in characters
listbox.grid_forget()  # Hide the listbox

# Create buttons
trainingBtn = tk.Button(app, text="Train", command=on_training_button_click)
trainingBtn.grid(row=0, column=0,sticky=tk.E+tk.W)
testingBtn = tk.Button(app, text="Test", command=on_testing_button_click)
testingBtn.grid(row=0, column=1,sticky=tk.E+tk.W)
eraseBtn = tk.Button(app, text="Erase", command=on_erase_button_click)
eraseBtn.grid(row=0,column=2,sticky=tk.E+tk.W)
saveBtn = tk.Button(app, text="Save", command=on_save_button_click)
saveBtn.grid(row=0, column=3,sticky=tk.E+tk.W)
guessBtn = tk.Button(app, text="Guess", command=on_guess_button_click)
guessBtn.grid(row=0, column=4,sticky=tk.E+tk.W)
settingsBtn = tk.Button(app, text="Settings", command=on_settings_button_click)
settingsBtn.grid(row=0,column=5,sticky=tk.E+tk.W)

# Create a Canvas widget for drawing
global canvas
canvas = tk.Canvas(app, bg="white", width=window_height-120, height=window_height-120)
canvas['state'] = tk.DISABLED
canvas.grid(row=2,column=1,columnspan=2)

# Bind mouse events to canvas
canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<B1-Motion>", on_canvas_drag)
listbox.bind("<<ListboxSelect>>", on_selection_changed)

# Start the event loop
app.mainloop()


