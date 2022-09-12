from cmath import sqrt
from tkinter import *
from turtle import width
import tkintermapview
import PySimpleGUI as sg
import json
from math import sqrt
mymarkers = []

#show a window to add a marker
def add_marker_event(coords):    
    layout = [[sg.Text("Insert the name"),sg.In(size=(25, 1), enable_events=True, key="place_name")], [sg.Radio("Red","RADIO1",default=True, key="color0")],[sg.Radio("Green","RADIO1",key="color1")],[sg.Radio("Blue","RADIO1",key="color2")],[sg.Radio("Yellow","RADIO1",key="color3")],[sg.Button("OK")]]
    window = sg.Window(title="Hello World", layout=layout, margins=(100, 50))   #create the window to insert the marker
    while True:
        event, values = window.read()   #show window and wait for results
        if event == "OK":
            #print(event," ",values)
            window.close()  #close window
            if(values["color0"]):   #get the marker color
                color="red"
            elif(values["color1"]):
                color="green"
            elif(values["color2"]):
                color="blue"
            else:
                color="yellow"
            new_marker = map_widget.set_marker(coords[0], coords[1], text=values["place_name"], marker_color_circle=color,marker_color_outside=color)   #create marker on map
            mymarkers.append(new_marker)
            
            f = open("markers.json", "r")
            data = json.load(f)
            data["markers"].append({    #save the new marker on the file
                'name':values["place_name"],
                'lat':coords[0],
                'lon':coords[1],
                'color':color
            })
            f.close()

            f = open("markers.json","w")
            f.write(json.dumps({"markers":data["markers"]}))
            f.close()
            
            break
        if event == sg.WIN_CLOSED:
            break

#get all the markers saved on a file and add them to the map
def add_marker_from_db(map_widget):
    """
    markers.json structure:
    {
        'markers':[
            {
                'name':...,
                'lat':...,
                'lon':...,
                'color':...
            },
            {
                ...
            }
        ]
    }
    """
    f = open("markers.json", "r")   #read the file containing all the markers and add them on the map
    data = json.load(f)
    for maker in data["markers"]:
        new_marker = map_widget.set_marker(maker["lat"], maker["lon"], text=maker["name"], marker_color_circle=maker["color"],marker_color_outside=maker["color"])   #create marker on map
        mymarkers.append(new_marker)
    f.close()

#remove a marker from the map (and the file) (choose the nearest marker from the clicked point)
def remove_marker_event(coords):
    maxdistance = 1.79e+308
    index_to_delete = -1
    for marker in mymarkers:
        distance = sqrt((coords[0]-marker.position[0])**2 + (coords[1]-marker.position[1])**2)
        if(distance < maxdistance): #save index of the nearest point
            maxdistance = distance
            index_to_delete = mymarkers.index(marker)

    

    f = open("markers.json", "r")   #read the file containing all the markers and remove the selected marker
    data = json.load(f)
    for marker in data["markers"]:
        if(marker["lat"] == mymarkers[index_to_delete].position[0] and marker["lon"] == mymarkers[index_to_delete].position[1]):
            data["markers"].remove(marker)
    f.close()

    f = open("markers.json", "w")   #write the updated list on the file
    f.write(json.dumps({"markers":data["markers"]}))
    f.close()

    mymarkers[index_to_delete].delete()
    mymarkers.remove(mymarkers[index_to_delete])

root = Tk()
root.geometry("1400x600")
root.resizable(False, False)



my_label = Frame(root)
my_label.pack(pady = 20)
my_label.grid_rowconfigure(100, weight=1)
my_label.grid_columnconfigure(2, weight=1)
map_widget = tkintermapview.TkinterMapView(my_label,width=800,height=600)
#map_widget.grid(row=0,column=0)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=18)
map_widget.set_position(41.5,12.28)
map_widget.set_zoom(1)
map_widget.pack(side="left",expand=False)#side="left", fill="both", expand=True


w = Label(root,text="Green: country visited\nRed: country to visit\nBlue: place to visit\nYellow: place visited\n").place(x=1150, y=5)
#w.pack(padx=5,pady=-200,side=RIGHT)#side="right", fill="both", expand=False
#w.grid(row=1,column=1)

add_marker_from_db(map_widget)  

map_widget.add_right_click_menu_command(label="Add Marker",command=add_marker_event,pass_coords=True)
map_widget.add_right_click_menu_command(label="Remove Marker",command=remove_marker_event,pass_coords=True)
root.mainloop()


## todo: 
# aggiungere legenda colori: rosso stati da visitare, verde stati visitati, blu, luoghi da visitare, giallo (?) luoghi visitati