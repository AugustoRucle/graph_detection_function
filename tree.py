#########################################################
#  Imports
#########################################################

from tkinter import *
from tkinter import ttk
from lecturaCodifoC import FunctionDetector
import random

#########################################################
# CONSTANT
#########################################################

INCREMENT_X = 100
INCREMENT_Y = 250
DIFFERENCE = 75
MULTI = 2

#########################################################
# Structs
#########################################################

dictionary_cicles = {}

#########################################################
# Globals
#########################################################

init_position_Y = 0
init_position_X = 0

#########################################################
# Functions
#########################################################

def circle (canvas, startX = 10, startY = 10, endX = 80, endY = 80, set_outline='#D9D9D9', set_color = '#737373', width = 2, name = ''):
        id = canvas.create_oval( startX, startY, endX, endY, 
                                        outline = set_outline, 
                                        fill = set_color, width = width )
        save_circle(name, startX, startY, endX, endY)
        return name

def text (canvas, x, y, text, font = ("bold", 10)):
        canvas.create_text (x, y, text = text, font = font)

def line(canvas, startX, startY, endX, endY):
        canvas.create_line(startX, startY, endX, endY, arrow=LAST)

def save_circle (id, startX, startY, endX, endY):
        dictionary_cicles[id] = { 
                "startX": startX, 
                "startY": startY,
                "endX"  : endX,
                "endY"  : endY
        }

def draw_graph(canvas, functions_total):
        print(functions_total)
        draw_node_father(canvas, functions_total)
        draw_conection(canvas, functions_total)
        # draw_node_father(canvas, functions_total)

def draw_conection(canvas, functions_total):
        for function_name, values in functions_total:
                for child in values:
                        line( canvas,
                              (dictionary_cicles[function_name]['startX'] + dictionary_cicles[function_name]['endX']) / 2 - 30,
                              (dictionary_cicles[function_name]['startY'] + dictionary_cicles[function_name]['endY']) / 2 ,
                              (dictionary_cicles[child]['startX'] + dictionary_cicles[child]['endX']) / 2 + 30,
                              (dictionary_cicles[child]['startY'] + dictionary_cicles[child]['endY']) / 2 + 20)


def draw_node_father(canvas, functions_total):
        later_id = 0
        for key, value in enumerate(functions_total):
                number_random = random.randint(0, 240)
                if(key == 0):
                        id = circle(canvas, startX= init_position + INCREMENT_X, 
                                        startY=init_position + INCREMENT_Y  + number_random, 
                                        endX=init_position + DIFFERENCE + INCREMENT_X, 
                                        endY=init_position +DIFFERENCE + INCREMENT_Y  + number_random, 
                                        name=value[0])

                        text(canvas, 
                                (dictionary_cicles[id]['startX'] + dictionary_cicles[id]['endX'] ) / 2, 
                                (dictionary_cicles[id]['startY'] + dictionary_cicles[id]['endY'] ) / 2,
                                value[0])
                        
                        later_id = id
                elif((key % 2) != 0):
                        id = circle(canvas, startX=dictionary_cicles[later_id]['startX'] + INCREMENT_X * MULTI, 
                                        startY=INCREMENT_Y  + number_random,
                                        endX=dictionary_cicles[later_id]['endX'] + INCREMENT_X * MULTI,
                                        endY=INCREMENT_Y + DIFFERENCE  + number_random,
                                        name=value[0])

                        text(canvas,
                                (dictionary_cicles[id]['startX'] + dictionary_cicles[id]['endX'] ) / 2, 
                                (dictionary_cicles[id]['startY'] + dictionary_cicles[id]['endY'] ) / 2,
                                value[0]) 
                        later_id = id    
                else:
                        id = circle(canvas, startX=dictionary_cicles[later_id]['startX'] + INCREMENT_X * MULTI, 
                                        startY=init_position + INCREMENT_Y,
                                        endX=dictionary_cicles[later_id]['endX'] + INCREMENT_X * MULTI,
                                        endY=init_position +DIFFERENCE + INCREMENT_Y,
                                        name=value[0])

                        text(canvas,
                                (dictionary_cicles[id]['startX'] + dictionary_cicles[id]['endX'] ) / 2, 
                                (dictionary_cicles[id]['startY'] + dictionary_cicles[id]['endY'] ) / 2,
                                value[0])
                        later_id = id
                      
def print_dictionary(dictionary):
    print("Printing dictionary..............\n\n")
    for key, value in enumerate ( dictionary.items() ):
        print(" k: {}, \n  Vs:{} \n".format(key, value))

#########################################################
# Main
#########################################################

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
h = Scrollbar(root, orient=HORIZONTAL)
v = Scrollbar(root, orient=VERTICAL)

# Creating Canvas

canvas = Canvas(root, scrollregion=(0, 0, 60000, 6000), yscrollcommand=v.set, xscrollcommand=h.set)
h['command'] = canvas.xview
v['command'] = canvas.yview

ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))
canvas.grid(column=0, row=0, sticky=(N,W,E,S))
h.grid(column=0, row=1, sticky=(W,E))
v.grid(column=1, row=0, sticky=(N,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

functions = FunctionDetector.start()
functions.append(('main', ['HashInsert', 'HashFind', 'HashPrint', 'HashDestroy']))
functions_total = len(functions)

init_position = (functions_total * DIFFERENCE) / 2


draw_graph(canvas, functions)

root.mainloop()


